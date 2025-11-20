import React, { useEffect, useState } from "react";
import Infographic from "@/components/infographic/Infographic";
import PageWrapper from "@/components/PageWrapper";
import { motion, AnimatePresence } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { TeleportBubble } from "@/components/TeleportBubble";

/**
 * Quiz page containing the interactive cyberbullying infographic visualization
 * and a button to navigate to the scenario game, with animated star background.
 * 
 * @page
 * @example
 * <QuizPage />
 */
const QuizPage: React.FC = () => {
  const [stars, setStars] = useState<{ id: number; x: number; y: number; size: number; opacity: number; blinkDuration: number; }[]>([]);
  const [showDialog, setShowDialog] = useState(true);
  const [dialogStep, setDialogStep] = useState(1);  


  // Speech bubble timeout ref to clear on new clicks
  const timeoutRef = React.useRef<ReturnType<typeof setTimeout> | null>(null); 

  // Generate random stars for the background
  useEffect(() => {
    const generateStars = () => {
      const newStars = [];
      const starCount = Math.floor(window.innerWidth * window.innerHeight / 10000) + 20;
      
      for (let i = 0; i < starCount; i++) {
        newStars.push({
          id: i,
          x: Math.random() * 100, // % position
          y: Math.random() * 100, // % position
          size: Math.random() * 2 + 1, // size between 1-3px
          opacity: Math.random() * 0.7 + 0.3, // opacity between 0.3-1
          blinkDuration: Math.random() * 3 + 2, // blink animation duration
        });
      }
      
      setStars(newStars);
    };

    generateStars();
    
    // Regenerate stars when window is resized
    window.addEventListener('resize', generateStars);
    return () => window.removeEventListener('resize', generateStars);
  }, []);
  
  // Auto-hide the speech bubble after a few seconds
    useEffect(() => {  
      runDialogSequence();
    
      return () => { 
        if (timeoutRef.current) clearTimeout(timeoutRef.current); 
      };
    }, []);
    
    const runDialogSequence = () => {
      setDialogStep(1);
      setShowDialog(true);
     
      // first timeout to hide the dialog after 3 seconds
      timeoutRef.current = setTimeout(() => {
        setShowDialog(false);
     
        // second timeout to show the dialog again after 2 seconds
        timeoutRef.current = setTimeout(() => {
          setDialogStep(2);
          setShowDialog(true);
    
          // Hide the dialog 
          timeoutRef.current = setTimeout(() => {
            setShowDialog(false);
          }, 5000);
        }, 2000);  
      }, 3000); 
    };

  // Handle character click
    const handleCharacterClick = () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
     
      runDialogSequence();
    }; 
   

  
  const navigate = useNavigate();

  // Navigation handler for teleport button
  const handleTeleportToNext = () => {
    navigate("/quiz-2");
  };

  const handleTeleportToBack = () => {
    navigate("/character-intro");
  };

  // const handleTeleportToBack = () => {
  //   navigate("/");
  // };
  
  return (
    <PageWrapper className="min-h-screen bg-gradient-to-b from-[#4DC0BE] to-[#23A2DA] text-white overflow-hidden relative">
      {/* Speech bubble styles */}
      <style dangerouslySetInnerHTML={{ __html: `
        .speech-bubble:before, .speech-bubble:after {
          position: absolute;
          z-index: -1;
          content: '';
        }
        
        .speech-bubble:after {
          top: 0; 
          right: 0; 
          bottom: 0; 
          left: 0;
          border-radius: inherit;
          transform: rotate(2deg) translate(.35em, -.15em) scale(1.02);
          background: #f4fbfe;
        }
        
        .speech-bubble:before {
          border: solid 0 transparent;
          border-right: solid 3.5em #f4fbfe;
          border-bottom: solid .25em #629bdd;
          bottom: .25em; 
          left: 1.25em;
          width: 0; 
          height: 1em;
          transform: rotate(45deg) skewX(75deg);
        }
      `}} />
      
      {/* Background Image */}
      <div className="absolute inset-0 z-0">
        <img 
          src="/quiz-class1.png" 
          alt="Classroom background"
          className="w-full h-full object-cover"
        />
      </div>
      
      {/* Star background */}
      <div className="absolute inset-0 z-0 overflow-hidden">
        {stars.map((star) => (
          <motion.div
            key={star.id}
            className="absolute rounded-full bg-white z-0"
            style={{
              left: `${star.x}%`,
              top: `${star.y}%`,
              width: `${star.size}px`,
              height: `${star.size}px`,
            }}
            animate={{
              opacity: [star.opacity, star.opacity * 0.3, star.opacity],
            }}
            transition={{
              duration: star.blinkDuration,
              repeat: Infinity,
              repeatType: "reverse",
            }}
          />
        ))}
      </div>
      
      {/* Character with speech bubble */}
      <div className="absolute left-20 bottom-10 h-full z-20 flex items-center">
        <div className="relative h-3/4 flex items-end mt-32">
          {/* Speech bubble */}
          <AnimatePresence>
            {showDialog && (
              <motion.div
                initial={{ opacity: 0, y: 20, scale: 0.9 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -20, scale: 0.9 }}
                transition={{ duration: 0.5 }}
                className="speech-bubble absolute"
                style={{
                  position: "absolute",
                  top: "100px",
                  left: "30px", /* Moved left from centered to directly above the character head */
                  transform: "none", /* Removed rotation and center transform */
                  borderRadius: "10px", /* More rounded corners like in the image */
                  boxShadow: "0 2px 8px rgba(0,0,0,0.1)", /* Light shadow */
                  margin: "0.5em 0", 
                  padding: "1em",
                  width: "15em", 
                  minHeight: "4em",
                  background: "#629bdd",
                  fontFamily: "Century Gothic, Verdana, sans-serif",
                  fontSize: "1.5rem",
                  textAlign: "center",
                  zIndex: 40,
                }}
              >
                <motion.div 
                  className="text-lg font-medium text-gray-800 z-10 relative"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ delay: 0.2, duration: 0.8 }}
                  style={{ position: "relative", zIndex: 5 }}
                >
                  {dialogStep === 1 ? "Count your classmates!" : "Count your classmates!"}
                </motion.div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Character */}
          <motion.div
            initial={{ x: -200, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{
              duration: 1.5,
              type: "spring",
              stiffness: 70,
              damping: 15
            }}
            className="relative"
          >
            <img 
              src="/character-book.gif" 
              alt="Character Guide" 
              className="h-full object-contain max-w-xs cursor-pointer"
              onClick={handleCharacterClick}
              style={{ zIndex: 30 }}
            />
          </motion.div>
        </div>
      </div>
      
      {/* Main content */}
      <div className="container mx-auto py-10 relative z-10">
        <div className="ml-32 md:ml-40 lg:ml-48">
          <Infographic />

          {/* Button wrapper */}
          <div className="mt-10 flex justify-center">
            <motion.div
              initial={{ opacity: 0, y: 100 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{
                duration: 2.2,
                delay: 0.3,
                type: "spring",
                stiffness: 100,
                damping: 10,
              }}
              className="relative"
            >
              {/* Shadow beneath the button */}
              <motion.div 
                className="absolute w-full h-4 bg-black/20 rounded-full blur-md bottom-0 left-0"
                animate={{
                  width: ['90%', '60%', '90%'],
                  x: ['5%', '20%', '5%']
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  repeatType: "reverse"
                }}
              />

            </motion.div>
          </div>
        </div>
      </div>
      
      {/* Teleport Bubble */}
      <TeleportBubble onClick={handleTeleportToNext} color="blue" position="right" text="2.Net Quiz" />
      <TeleportBubble onClick={handleTeleportToBack} color="purple" position="left" text="Intro" />
    </PageWrapper>
  );
};

export default QuizPage;