import React, { useEffect, useState } from 'react';
import { useInfographicViewModel } from '@/hooks/useInfoGraphic';
import { motion } from 'framer-motion';
import { cn } from '@/lib/utils';
import './Infographic.css';

/**
 * Interactive visualization demonstrating cyberbullying statistics.
 * Takes user input for class size and generates a visual representation
 * of how many students might be experiencing cyberbullying.
 * 
 * @component
 * @example
 * <Infographic />
 */
const Infographic: React.FC = () => {
  const {
    state,
    audioRef,
    gridRef,
    handleStudentCountChange,
    generateIcons,
    getIconSrc,
    calculateIconSize
  } = useInfographicViewModel();

  
  const { studentCount, showCaptions, icons, isAnimating, currentStep } = state;
  
  // Calculate icon size based on student count
  const iconSize = calculateIconSize(studentCount);
  
  // Tooltip texts for different icon states
  const tooltipTexts = {
    normal: "It's great that you haven't experienced bullying, but it's important to be aware and supportive of others who might be going through it.",
    orange: "You may feel isolated or afraid to speak up, but you're not alone. It's important to reach out to someone you trust.",
    maroon: "Talking to your parents is a great first step in getting the support you need. They care about you and want to help."
  };
  
  /**
   * Updates grid layout when student count changes
   * 
   * @effect
   * @dependency {number} iconSize - Current calculated icon size
   * @dependency {number} studentCount - Number of students entered by user
   */
  useEffect(() => {
    if (gridRef.current && studentCount > 0) {
      gridRef.current.style.gridTemplateColumns = `repeat(auto-fill, minmax(${iconSize}px, 1fr))`;
    }
  }, [gridRef, iconSize, studentCount]);
  
  /**
   * Updates state when input value changes
   * 
   * @param {React.ChangeEvent<HTMLInputElement>} e - Input change event
   */
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = parseInt(e.target.value, 10);
    handleStudentCountChange(isNaN(value) ? 0 : value);
  };
  
  /**
   * Validates user input and starts the visualization sequence
   * Shows an alert if value is outside valid range (10-200)
   */
  const handleSubmit = () => {
    if (isAnimating) return;
    
    if (isNaN(studentCount) || studentCount < 10 || studentCount > 200) {
      alert("Enter a number between 10 and 200");
      return;
    }
    
    generateIcons(studentCount);
  };

  // Button variants similar to PrimaryButton component
  const buttonVariants = {
    initial: {
      scale: 1,
    },
    hover: {
      scale: 1.05,
      transition: { duration: 0.3 }
    },
    tap: {
      scale: 0.95,
      transition: { duration: 0.1 }
    }
  };

  // Particle animation for when button is clicked
  const [showParticles, setShowParticles] = useState(false);
  
  const handleButtonClick = () => {
    setShowParticles(true);
    handleSubmit();
    
    // Hide particles after animation completes
    setTimeout(() => setShowParticles(false), 1000);
  };
  
  return (
    <div className="flex flex-col items-center justify-center space-y-6 p-8 w-full max-w-4xl mx-auto relative">
      {/* Simplified CSS styles */}
      <style>{`
        /* Basic animations */
        @keyframes float {
          0% { transform: translateY(0px); }
          50% { transform: translateY(-10px); }
          100% { transform: translateY(0px); }
        }
        
        /* Glass container effect */
        .glass-container {
          background: rgba(255, 255, 255, 0.15);
          backdrop-filter: blur(5px);
          border-radius: 20px;
          border: 2px solid rgba(255, 255, 255, 0.2);
          box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
        }
        
        /* Input styles */
        .input-field {
          background: white;
          border: 2px solid #C2E764;
          border-radius: 15px;
          color: #000;
          font-size: 20px;
          font-weight: normal;
          text-align: center;
          width: 150px;
          height: 55px;
          transition: all 0.2s ease;
          box-shadow: 0 4px 0 rgba(0, 0, 0, 0.1);
        }
        
        .input-field:focus {
          outline: none;
          border-color: #C2E764;
          box-shadow: 0 6px 0 rgba(0, 0, 0, 0.1);
        }
        
        /* Caption container */
        .caption-container {
          background: linear-gradient(135deg, #184D97 0%, #184D97 20%, #1E88E5 100%);
          padding: 1.5rem;
          border-radius: 15px;
          position: relative;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
          border: 2px solid rgba(106, 136, 255, 0.5);
        }
        
        /* Hover effect for icons */
        .icon-hover {
          transition: all 0.2s ease;
        }
        
        .icon-hover:hover {
          transform: scale(1.1);
          z-index: 10;
        }
        
        /* Particle animation */
        .particles {
          position: absolute;
          left: 0;
          right: 0;
          top: 0;
          bottom: 0;
          pointer-events: none;
        }
        
        .particle {
          position: absolute;
          width: 10px;
          height: 10px;
          background: #C2E764;
          border-radius: 50%;
          animation: particle-animation 1s forwards cubic-bezier(0.175, 0.885, 0.32, 1.275);
          opacity: 1;
        }
        
        @keyframes particle-animation {
          100% {
            transform: translate(var(--tx), var(--ty)) scale(0);
            opacity: 0;
          }
        }
      `}</style>
      
      {/* Particles for button click */}
      {showParticles && (
        <div className="particles">
          {Array.from({ length: 30 }).map((_, i) => {
            const angle = Math.random() * Math.PI * 2;
            const speed = 50 + Math.random() * 150;
            const tx = Math.cos(angle) * speed;
            const ty = Math.sin(angle) * speed;
            const size = 5 + Math.random() * 15;
            const duration = 0.5 + Math.random() * 0.5;
            const delay = Math.random() * 0.2;
            const color = [
              '#C2E764', '#A9FB4E', '#FFDE59', '#FF914D', '#59EEEE'
            ][Math.floor(Math.random() * 5)];
            
            return (
              <div 
                key={i}
                className="particle"
                style={{
                  '--tx': `${tx}px`,
                  '--ty': `${ty}px`,
                  width: `${size}px`,
                  height: `${size}px`,
                  left: '50%',
                  top: '50%',
                  background: color,
                  animation: `particle-animation ${duration}s forwards cubic-bezier(0.175, 0.885, 0.32, 1.275)`,
                  animationDelay: `${delay}s`
                } as React.CSSProperties}
              />
            );
          })}
        </div>
      )}
      
      <motion.h1 
        className="text-center text-3xl md:text-4xl font-bold text-white -mt-[2cm]"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7 }}
      >
        <motion.span 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4, duration: 0.7 }}
          className="block mt-3 text-2xl md:text-3xl font-bold "
        >
          How many students hang out in your class?
        </motion.span>
      </motion.h1>
      
      {icons.length === 0 && (
    <motion.div 
      className="glass-container flex flex-col sm:flex-row items-center gap-5 p-7 mx-auto"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.6, duration: 0.7 }}
      style={{ maxWidth: "500px", transform: "translateX(-60px)" }}
    >
      <motion.div
        animate={{ y: [0, -5, 0] }}
        transition={{ duration: 2.5, repeat: Infinity, ease: "easeInOut" }}
      >
        <input
          className="input-field"
          type="number"
          min="10"
          max="200"
          placeholder="?"
          value={studentCount || ''}
          onChange={handleInputChange}
        />
      </motion.div>

      <div className="relative">
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
        
        <motion.button
          className={cn(
            'relative font-bold rounded-full px-8 py-4 shadow-lg z-10',
            'bg-[#C2E764] text-black -rotate-6 hover:rotate-0',
          )}
          variants={buttonVariants}
          initial="initial"
          whileHover="hover"
          whileTap="tap"
          animate={{ y: [0, -8, 0] }}
          transition={{
            y: {
              duration: 1.2,
              repeat: Infinity,
              ease: "easeInOut"
            }
          }}
          onClick={handleButtonClick}
          disabled={isAnimating}
        >
          {isAnimating ? 'Getting Facts...' : 'Show Me!'}

          {/* Ring orbits */}
          <motion.div
            className="absolute inset-0 border-2 border-black/10 rounded-full"
            animate={{ scale: [1, 1.1, 1], opacity: [0.7, 0.5, 0.7] }}
            transition={{ duration: 3, repeat: Infinity }}
          />
          <motion.div
            className="absolute inset-0 border-2 border-black/5 rounded-full"
            animate={{ scale: [1, 1.2, 1], opacity: [0.5, 0.3, 0.5] }}
            transition={{ duration: 3, delay: 0.2, repeat: Infinity }}
          />
        </motion.button>
      </div>
    </motion.div>
  )}
        
        {/* Grid for student icons */}
        <motion.div 
          ref={gridRef}
          initial={{ opacity: 0 }}
          animate={{ opacity: icons.length > 0 ? 1 : 0 }}
          transition={{ duration: 0.5 }}
          className="grid gap-2 justify-center w-full max-w-3xl mt-18 rounded-xl p-6 shadow-lg"
          style={{
            backgroundColor: ' rgba(143, 175, 217, 0.9)', 
            border: '2px solid rgba(230, 218, 203, 0.5)',
            borderRadius: '20px',
            padding: '2rem',
          }}
        >
          {icons.map((icon, index) => (
            <motion.img
              key={icon.id}
              src={getIconSrc(icon.gender, icon.state)}
              initial={{ scale: 0 }}
              animate={{ 
                scale: 1,
                transition: { 
                  type: 'spring', 
                  stiffness: 200, 
                  damping: 10,
                  delay: index * 0.01 // Staggered appearance
                } 
              }}
              className={`icon-hover transition-all duration-300 ${
                icon.highlighted ? 'brightness-120 scale-105 z-10' : ''
              }`}
              style={{ width: iconSize, height: iconSize }}
              title={tooltipTexts[icon.state]}
              alt={`${icon.gender} icon`}
              whileHover={{ 
                scale: 1.1,
                transition: { duration: 0.2 } 
              }}
            />
          ))}
        </motion.div>
        
        {/* Animated caption container */}
        {showCaptions && (
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7 }}
            className="caption-container w-full max-w-[600px]"
          >
            <div className={`caption ${currentStep === 1 ? 'show orange' : 'hide'}`}>
              30% of students have experienced cyberbullying.
            </div>
            
            <div className={`caption ${currentStep === 2 ? 'show orange' : 'hide'}`}>
              Girls are more likely than boys to be targeted.
            </div>
            
            <div className={`caption ${currentStep === 3 ? 'show maroon' : 'hide'}`}>
              Only one in five who face cyberbullying share their pain with their parents.
            </div>
            
            <div className={`caption ${currentStep === 4 ? 'show blue' : 'hide'}`}>
              You don't have to face this alone - reach out for support.
            </div>
            
            <div className={`caption ${currentStep === 5 ? 'show blue' : 'hide'}`}>
              Talk to an adult, and together we can stop it!
            </div>
          </motion.div>
        )}
        
        {/* Sound effect for icon transitions */}
        <audio 
          ref={audioRef}
          src="/quizPage/95265__department64__tree_pop.wav"
          preload="auto"
        />
        
        {/* Reset button appears after animation completes */}
        {false && !isAnimating && showCaptions && (
  <div className="relative">
    {/* button "Discover App Dangers!" */}
  </div>
)}
      </div>
  );
};

export default Infographic;