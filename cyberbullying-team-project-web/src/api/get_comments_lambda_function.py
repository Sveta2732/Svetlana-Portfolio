import mysql.connector
import json
import random
import os

def lambda_handler(event, context):
    """
    AWS Lambda handler:
    - Connects to AWS RDS MySQL database
    - Fetches all comments from COMMENT2 table
    - Shuffles comments, grouping them to ensure balanced distribution:
        * 4 positive comments
        * 6 non-positive comments
      (Repeated until not enough comments remain)
    - Returns comments in JSON format with CORS headers
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

    # Fetch comment fields
    cursor = connection.cursor()
    cursor.execute("SELECT comment_id, comment_text, comment_fake_user, comment_status FROM COMMENT2")
    results = cursor.fetchall()
    # Shuffle original results
    random.shuffle(results)

    # Split into two groups based on comment_status
    positive_comments = [comment for comment in results if comment[3] == 'positive']
    other_comments = [comment for comment in results if comment[3] != 'positive']


    shuffled_comments = []

    # Create balanced blocks: 4 positive + 6 other
    while len(positive_comments) >= 4 and len(other_comments) >= 6:
        
        block_positive = positive_comments[:4]
        positive_comments = positive_comments[4:]
        
        
        block_other = other_comments[:6]
        other_comments = other_comments[6:]
        
        # Merge and shuffle each block
        block = block_positive + block_other
        random.shuffle(block)
        
        
        shuffled_comments.extend(block)

    # Add remaining comments (if any)
    shuffled_comments.extend(positive_comments)
    shuffled_comments.extend(other_comments)

    cursor.close()
    connection.close()
    
    # Build API response
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        # Convert each tuple into a JSON object
        'body': json.dumps({
            
             'Comments': list(map(lambda x: {
                 'comment_id': x[0],
                 'comment_text': x[1],
                 'comment_fake_name': x[2],
                 
            }, results))
        })
    }