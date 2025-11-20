import mysql.connector
import json
import os

def lambda_handler(event, context):
    """
    AWS Lambda function for processing user submissions in the Cyberbullying Game.
    
    Responsibilities:
    - Connect to MySQL database using secure environment variables.
    - Validate user responses against comment labels.
    - Calculate score and summary feedback.
    - Identify weak areas (e.g., gender bullying, positive comments, etc.).
    - Save submission + user responses into the database.
    - Return score breakdown and mistakes to frontend.
    """
        
    # Read credentials from environment variables
    db_host = os.environ.get("DB_HOST")
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")

    
    # Connect to the RDS MySQL database
    connection = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database='cyberbullying'
    )
    
    # Parse incoming request body
    body = json.loads(event['body'])
    print(body)

    # Extract comment IDs from submission
    comment_ids = list(map(lambda x: x["comment_id"], body['submission']))
    print(comment_ids)
    
    answered = len(comment_ids)

    cursor = connection.cursor()
    # Retrieve correct labels for the submitted comments
    placeholders = ','.join(['%s'] * len(comment_ids))
    sql = f"SELECT comment_id, comment_status FROM COMMENT2 WHERE comment_id IN ({placeholders})"
    cursor.execute(sql, comment_ids)
    results = cursor.fetchall()
    print(results)

    # Collect IDs of incorrect answers
    mistakes = []

    # Match each submitted comment with DB record
    for dict in body['submission']:
        matching = None
        for part in results:
            if dict['comment_id'] == part[0]:
                matching = part
                dict['comment_status'] = part[1]

        # Determine correctness based on user's response
        if dict['response_status'] == 'like' and matching[1].strip() == 'positive':
            dict['answer'] = 'correct'
        elif dict['response_status'] == 'dislike' and matching[1].strip() != 'positive':
            dict['answer'] = 'correct'
        else:
            dict['answer'] = 'incorrect'
            mistakes.append(dict['comment_id'])
    
     # Fetch text + bullying category for incorrect answers
    cursor = connection.cursor()
    # Convert all non-positive statuses into "bullying" for display
    full_results = []
    if mistakes:
        placeholders2 = ','.join(['%s'] * len(mistakes))
        sql = f"SELECT comment_text, comment_status FROM COMMENT2 WHERE comment_id IN ({placeholders2})"
        cursor.execute(sql, mistakes)
        results2 = cursor.fetchall()
        full_results = [
        (comment_text, comment_status if comment_status == 'positive' else 'bullying')
        for comment_text, comment_status in results2
        ]

    # Summary scoring logic
    print(body['submission'])
    answers = list(map(lambda x: x["answer"], body['submission']))
    correct_answers = [a for a in answers if a =='correct']
       
    answered_cor = len(correct_answers)
    percent = (answered_cor/answered)*100
    # Scoring formula: reward correct answers, penalize mistakes, no negative score
    calc_score = 10*answered_cor - 5*(answered - answered_cor)
    score = max(calc_score, 0)
    print(answered, answered_cor)
    
    # Count incorrect answers by bullying category
    status_counts = {}

    for d in body['submission']:
        status = d['comment_status']
        answer = d['answer']
    
        if status not in status_counts:
            status_counts[status] = {'total': 0, 'incorrect': 0}
        
        status_counts[status]['total'] += 1
        if answer == 'incorrect':
            status_counts[status]['incorrect'] += 1

    # Identify category where user struggles the most
    max_incorrect_status = None
    max_incorrect_percent = -1

    for status, counts in status_counts.items():
        total = counts['total']
        incorrect = counts['incorrect']
        if total > 0:
            incorrect_percent = incorrect / total
            if incorrect_percent > max_incorrect_percent and incorrect > 0:
                max_incorrect_percent = incorrect_percent
                max_incorrect_status = status

    # Generate personalized feedback message
    if max_incorrect_status is None:
        message = (
            "Congratulations! You have an excellent understanding of cyberbullying. "
            "You did not make a single mistake in recognizing bullying comments!"
        )
    elif max_incorrect_status == 'positive':
        message = (
            "Growth Area: Recognizing non-bullying comments. "
            "It seems you sometimes identify harmless messages as bullying. "
            "It's good to be cautious, but remember — not every negative expression is cyberbullying. "
            "Try to distinguish between serious harassment and simple disagreement."
        )
    elif max_incorrect_status == 'general negative':
        message = (
            "Growth Area: Detecting offensive behavior. "
            "You sometimes missed comments that were actually bullying. "
            "Remember that even general insults and offensive language can be forms of cyberbullying."
        )
    elif max_incorrect_status == 'gender':
        message = (
            "Growth Area: Identifying gender-based bullying. "
            "You may have overlooked bullying related to gender identity. "
            "Pay attention to comments that target or stereotype people based on their gender."
        )
    elif max_incorrect_status == 'age':
        message = (
            "Growth Area: Recognizing age-based bullying. "
            "Bullying related to someone's age can be subtle but harmful. "
            "Be mindful of jokes or comments that mock someone's age or stage of life."
        )
    elif max_incorrect_status == 'nationality':
        message = (
            "Growth Area: Spotting nationality-related bullying. "
            "You might have missed comments that targeted someone's nationality or cultural background. "
            "Discrimination based on nationality is a serious form of cyberbullying."
        )
    elif max_incorrect_status == 'socioeconomic':
        message = (
            "Growth Area: Recognizing bullying based on socioeconomic status. "
            "Comments that mock someone's financial situation or social class are forms of bullying. "
            "Be sensitive to how money and status are discussed online."
        )
    elif max_incorrect_status == 'educational':
        message = (
            "Growth Area: Identifying education-based bullying. "
            "Making fun of someone's education level, knowledge, or academic success is also bullying. "
            "Look closely for comments that shame or belittle people for their learning."
        )
    elif max_incorrect_status == 'physical':
        message = (
            "Growth Area: Spotting physical appearance-based bullying. "
            "Teasing or insulting someone's physical appearance is a very common form of bullying. "
            "Be alert to comments about body image, disability, or physical traits."
        )
    else:
        message = (
            "You did a good job overall! However, pay extra attention to the following area: "
            f"{max_incorrect_status}."
        )
    
    # Save submission summary to DB
    sql = f"INSERT INTO SUBMISSION (sub_answered, sub_correct, sub_correct_score) VALUES (%s, %s, %s)"
    cursor.execute(sql, (answered,answered_cor, score))
    connection.commit()
    submission_id = cursor.lastrowid
    # Save each individual response
    for dic in body['submission']:
        sql = f"INSERT INTO RESPONSE (comment_id, submission_id, response_status, response_time, correctness) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (dic['comment_id'], submission_id, dic['response_status'], dic['response_time'], dic['answer']))

    connection.commit()

    # fetch the count of the total number of submissions
    cursor.execute("SELECT COUNT(*) FROM SUBMISSION")
    count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM SUBMISSION WHERE sub_correct_score <= %s", (score,))
    lower = cursor.fetchone()[0]
    print(count, lower)

    cursor.close()
    connection.close()
    
    # Final response returned to frontend
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps({
            "mistakes": full_results,
            "problem": max_incorrect_status,
            'summary': message,
            "score": score,
            "answered": answered,
            "answered_cor": answered_cor,
            "percent": f"{round(percent, 1)}%",
            "submission_id": submission_id,
            "comparison": f"{round(lower/count*100, 1)}"
        })
    }