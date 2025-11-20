// This component displays an interactive social media selection page.
// When the user chooses a platform, a sequence of animated text tips appears,
// explaining cyberbullying statistics and providing reporting resources.

import React from 'react';
import { TeleportBubble } from "@/components/TeleportBubble";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { AnimatePresence, motion } from "framer-motion";

interface TextItem {
  text: string;
  color: string;
  delay: number;
}

const SocialMediaQuestion: React.FC = () => {
  const [selected, setSelected] = useState<string>("");
  const [showResult, setShowResult] = useState<boolean>(false);
  const [currentText, setCurrentText] = useState<string>("");
  const [textColor, setTextColor] = useState<string>("white");
  const [gifKey, setGifKey] = useState<number>(0);
  const [showBubble, setShowBubble] = useState<boolean>(true);
  const [secondaryText, setSecondaryText] = useState<string>("");

  const navigate = useNavigate();


  // Auto-hide the intro speech bubble after a delay.
  useEffect(() => {
    if (showBubble) {
      const timer = setTimeout(() => {
        setShowBubble(false);
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [showBubble]);

  // Handle animated text sequence for Facebook selection.
  // Each message has a specific delay to create a storytelling effect.
  useEffect(() => {
    if (showResult && selected === "facebook") {
      const textSequence: TextItem[] = [
        { text: "A lot of my friends said Facebook was cool… I want to download this one!", color: " #1e3a8a", delay: 0 },
        { text: "Did you know that in Australia, 37% of kids using Facebook have experienced cyberbullying?", color: "#D32F2F", delay: 4000 },
        { text: "And 47% — almost half — have seen it happen to someone else.", color: "#A349A4", delay: 8300 },
        { text: "Just because Facebook is popular doesn't mean it's always safe — use it wisely.", color: "#1e3a8a", delay: 12000 },
        { text: "If something feels wrong, report it and say someone you trust. Don't stay silent.", color: "#1e3a8a", delay: 15000 }
      ];

      setSecondaryText("<a href=\"https://www.facebook.com/help/200526129992122/list/\" target=\"_blank\" class=\"underline text-blue-800 font-semibold\">Report on Facebook<span>↗</span></a>");

      textSequence.forEach(({ text, color, delay }) => {
        setTimeout(() => {
          setCurrentText(text);
          setTextColor(color);
        }, delay);
      });

      setTimeout(() => {
        setShowResult(false);
        setCurrentText("");
        setSelected("");
      }, 19000);
    }
  }, [showResult, selected]);

  // Same storytelling logic for Instagram: timed messages + dynamic colors.
  // The sequence highlights cyberbullying statistics on the platform.
  useEffect(() => {
    if (showResult && selected === "instagram") {
      const textSequence: TextItem[] = [
        { text: "Instagram looks fun! Time to install it and check it out!", color: " #1e3a8a", delay: 0 },
        { text: "I didn't expect it, but 31% of Aussie teens have been bullied on this app.", color: "#D32F2F", delay: 4000 },
        { text: "34% of kids saw others being bullied — and many didn't know what to do.", color: "#A349A4", delay: 8300 },
        { text: "Social media isn't bad — but silence can be. ", color: "#1e3a8a", delay: 12000 },
        { text: "You're not alone. There are tools to help — and people who care.", color: "#1e3a8a", delay: 15000 }
      ];
      setSecondaryText("<a href=\"https://help.instagram.com/\" target=\"_blank\" class=\"underline text-blue-800 font-semibold\">Report on Instagram<span>↗</span></a>");



      textSequence.forEach(({ text, color, delay }) => {
        setTimeout(() => {
          setCurrentText(text);
          setTextColor(color);
        }, delay);
      });

      setTimeout(() => {
        setShowResult(false);
        setCurrentText("");
        setSelected("");
      }, 19000);
    }
  }, [showResult, selected]);


  // WhatsApp-specific animated sequence.
  // The delays create a flowing narrative synchronized with GIF animation.
  useEffect(() => {
  if (showResult && selected === "whatsapp") {
    const textSequence: TextItem[] = [
      { text: "Group chats, stickers, and endless messages? Yep, this one's for me.", color: " #1e3a8a", delay: 0 },
      { text: "Okay… just found out that 18% of kids have been targeted in chats. Not so friendly after all.", color: "#D32F2F ", delay: 4000 },
      { text: "And it gets worse — nearly 1 in 5 teens have seen bullying here, even if it wasn't about them.", color: "#A349A4", delay: 8300 },
      { text: "Guess bullying can hide anywhere — even in everyday apps like this — speak up if you see it.", color: "#1e3a8a", delay: 14000 }
    ];
    setSecondaryText("<a href=\"https://faq.whatsapp.com/1313491802751163/?locale=en_US&category=5245250\" target=\"_blank\" class=\"underline text-blue-800 font-semibold\">Report on WhatsApp<span>↗</span></a>");


    textSequence.forEach(({ text, color, delay }) => {
      setTimeout(() => {
        setCurrentText(text);
        setTextColor(color);
      }, delay);
    });

    setTimeout(() => {
      setShowResult(false);
      setCurrentText("");
      setSelected("");
    }, 18000);
  }
}, [showResult, selected]);

// Snapchat animated message flow with dynamic colors and safety links.
useEffect(() => {
  if (showResult && selected === "snapchat") {
    const textSequence: TextItem[] = [
      { text: "Let's see what the filters do to my antenna!", color: " #1e3a8a", delay: 0 },
      { text: "Whoa… 34% of teens got bullied on Snapchat? That's way more than I expected.", color: "#D32F2F", delay: 4000 },
      { text: "Okay… not just fun and filters.", color: "#1e3a8a", delay: 8300 },
      { text: "Makes sense. Use it, enjoy it — but speak up if it crosses the line. Staying silent just lets it keep going", color: "#1e3a8a", delay: 11000 }
    ];
    setSecondaryText("<a href=\"https://support.snapchat.com/\" target=\"_blank\" class=\"underline text-blue-800 font-semibold\">Report on Snapchat<span>↗</span></a>");


    textSequence.forEach(({ text, color, delay }) => {
      setTimeout(() => {
        setCurrentText(text);
        setTextColor(color);
      }, delay);
    });

    setTimeout(() => {
      setShowResult(false);
      setCurrentText("");
      setSelected("");
    }, 16000);
  }
}, [showResult, selected]);

  // Navigation between steps using React Router.
  // Used for storyline progression across the web app.
  // Navigation handler for teleport button
  const handleTeleportToNext = () => {
    navigate("/story");
  };

  const handleTeleportToBack = () => {
    navigate(-1);
  };

  // Main component rendering:
  // - Intro bubble with animation
  // - Dropdown selection UI
  // - Animated GIF + timed educational messages
  // - Safety link (dangerouslySetInnerHTML used to allow clickable links)
  // - Teleport navigation bubbles
  return (
    <div
      className="min-h-screen w-screen bg-cover bg-center flex flex-col items-center justify-start relative"
      style={{ backgroundImage: "url('/space1.png')" }}
    >
      {!showResult && (
          <>
          <div onClick={() => setShowBubble(true)}>
            <img
              src="/gleepo1.gif"
              alt="Gleepo"
              className="absolute bottom-4 left-4 w-130 h-130"
            />
          </div>
          <AnimatePresence>
            {showBubble && (
              <motion.div
                initial={{ opacity: 0, y: 20, scale: 0.9 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: -20, scale: 0.9 }}
                transition={{ duration: 0.5 }}
                className="absolute left-[9rem] bottom-[28rem] text-black text-lg font-medium z-20"
                style={{
                  position: "absolute",
                  padding: "1em",
                  width: "15em",
                  minHeight: "4em",
                  borderRadius: "0.25em",
                  transform: "rotate(-4deg) rotateY(15deg)",
                  background: "#629bdd",
                  fontFamily: "Century Gothic, Verdana, sans-serif",
                  fontSize: "1.3rem",
                  textAlign: "center"
                }}
              >
                <div
                  style={{
                    position: "absolute",
                    zIndex: -1,
                    top: 0,
                    right: 0,
                    bottom: 0,
                    left: 0,
                    borderRadius: "0.25em",
                    transform: "rotate(2deg) translate(.35em, -.15em) scale(1.02)",
                    background: "#f4fbfe"
                  }}
                />
                <div
                  style={{
                    position: "absolute",
                    zIndex: -1,
                    border: "solid 0 transparent",
                    borderRight: "solid 3.5em #f4fbfe",
                    borderBottom: "solid .25em #629bdd",
                    bottom: ".25em",
                    left: "1.25em",
                    width: 0,
                    height: "1em",
                    transform: "rotate(45deg) skewX(75deg)"
                  }}
                />
                Hey, what social media app do you think I should try? Got a favorite?
              </motion.div>
            )}
          </AnimatePresence>
        </>
      )}

      <h1 className="pt-10 text-white text-3xl font-bold text-center">
        <span className="px-4 py-1">
          What is your favorite social media platform?
        </span>
      </h1>

      {!showResult && (
        <div className="flex flex-col items-center mt-10 p-6 rounded-2xl border-2 border-white/30 bg-white/10 backdrop-blur-md shadow-xl z-10 max-w-md mx-auto">
          <div className="mb-4 w-full">
            <Select onValueChange={(value) => setSelected(value)}>
              <SelectTrigger className="w-full bg-white text-black border-2 border-[#C2E764] rounded-[15px] font-normal text-lg text-center shadow-md focus:outline-none focus:border-[#C2E764] focus:shadow-md transition-all duration-200 h-14">
                <SelectValue placeholder="Choose a platform" />
              </SelectTrigger>
              <SelectContent className="bg-white/95 backdrop-blur-md border-2 border-[#C2E764] rounded-[15px]">
                <SelectGroup>
                  <SelectItem value="facebook" className="text-lg py-2 focus:bg-[#C2E764]/20">Facebook</SelectItem>
                  <SelectItem value="instagram" className="text-lg py-2 focus:bg-[#C2E764]/20">Instagram</SelectItem>
                  <SelectItem value="whatsapp" className="text-lg py-2 focus:bg-[#C2E764]/20">WhatsApp</SelectItem>
                  <SelectItem value="snapchat" className="text-lg py-2 focus:bg-[#C2E764]/20">Snapchat</SelectItem>
                </SelectGroup>
              </SelectContent>
            </Select>
          </div>
          
          <motion.button
            className={[
              'relative font-bold rounded-full px-10 py-3 mt-2 shadow-lg z-10 text-lg',
              'bg-[#C2E764] text-black -rotate-3 hover:rotate-0 transition-all duration-300',
              !selected ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer hover:scale-105'
            ].join(' ')}
            disabled={!selected}
            animate={{ y: [0, -6, 0] }}
            transition={{
              duration: 1.5,
              repeat: Infinity,
              ease: "easeInOut"
            }}
            onClick={() => {
              setShowResult(false);
              setCurrentText("");
              setGifKey(Date.now());
              setTimeout(() => setShowResult(true), 20);
            }}
          >
            {!selected ? 'Select a platform' : 'Show me'}
            
            {/* Add subtle orbiting glow effect around button */}
          </motion.button>
        </div>
      )}

      // Conditional rendering for the selected platform.
      // Each platform loads its own GIF and message container layout.
      {showResult && selected === "facebook" && (
        <div className="flex items-start justify-center h-full pt-20 gap-8">
          <img key={gifKey} src={`/facebook1.gif?${gifKey}`} alt="Facebook" className="w-[41rem] h-[41rem] object-contain translate-x-[-3cm]" />
          <div className="fixed w-[28rem]" style={{ top: "calc(50% - 1cm)", right: "6%" }}>
        <div className="p-4 rounded-[20px] text-2xl border-4 border-cyan-400 shadow-xl"
          style={{
            background: "linear-gradient(180deg, #a0f0f9 0%, #b8f6e9 90%, #c2fbd7 100%)",
            backdropFilter: "blur(4px)",
          }}>
          <p style={{ color: textColor, fontWeight: 'bold' }}>{currentText}</p>
        </div>
        <div className="p-4 rounded-[20px] text-lg border-4 shadow-xl absolute"
          style={{
            top: "5cm",
            marginTop: "-4cm",
            transform: "translateY(4cm)",
            width: "fit-content",
            maxWidth: "100%",
            background: "white",
            border: "3px solid #C2E764",
          }}>
          <p className="text-black font-medium" dangerouslySetInnerHTML={{ __html: secondaryText }} />
        </div>
      </div>
        </div>
      )}

      {showResult && selected === "instagram" && (
        <div className="flex items-start justify-center h-full pt-20 gap-8">
          <img key={gifKey} src={`/insta1.gif?${gifKey}`} alt="Instagram" className="w-[41rem] h-[41rem] object-contain translate-x-[-3cm]" />
          <div className="fixed w-[28rem]" style={{ top: "calc(50% - 1cm)", right: "6%" }}>
          <div className="p-4 rounded-[20px] text-2xl border-4 border-cyan-400 shadow-xl"
            style={{
              background: "linear-gradient(180deg, #a0f0f9 0%, #b8f6e9 90%, #c2fbd7 100%)",
              backdropFilter: "blur(4px)",
            }}>
            <p style={{ color: textColor, fontWeight: 'bold' }}>{currentText}</p>
          </div>
          <div className="p-4 rounded-[20px] text-lg border-4 shadow-xl absolute"
            style={{
              top: "5cm",
              marginTop: "-4cm",
              transform: "translateY(4cm)",
              width: "fit-content",
              maxWidth: "100%",
              background: "white",
              border: "3px solid #C2E764",
            }}>
            <p className="text-black font-medium" dangerouslySetInnerHTML={{ __html: secondaryText }} />
          </div>
        </div>
        </div>
      )}

      {showResult && selected === "whatsapp" && (
        <div className="flex items-start justify-center h-full pt-20 gap-8">
          <img key={gifKey} src={`/whatsapp1.gif?${gifKey}`} alt="WhatsApp" className="w-[41rem] h-[41rem] object-contain translate-x-[-3cm]" />
          <div className="fixed w-[28rem]" style={{ top: "calc(50% - 1cm)", right: "6%" }}>
          <div className="p-4 rounded-[20px] text-2xl border-4 border-cyan-400 shadow-xl"
            style={{
              background: "linear-gradient(180deg, #a0f0f9 0%, #b8f6e9 90%, #c2fbd7 100%)",
              backdropFilter: "blur(4px)",
            }}>
            <p style={{ color: textColor, fontWeight: 'bold' }}>{currentText}</p>
          </div>
          <div className="p-4 rounded-[20px] text-lg border-4 shadow-xl absolute"
            style={{
              top: "5cm",
              marginTop: "-4cm",
              transform: "translateY(4cm)",
              width: "fit-content",
              maxWidth: "100%",
              background: "white",
              border: "3px solid #C2E764",
            }}>
            <p className="text-black font-medium" dangerouslySetInnerHTML={{ __html: secondaryText }} />
          </div>
        </div>
        </div>
      )}

      {showResult && selected === "snapchat" && (
        <div className="flex items-start justify-center h-full pt-20 gap-8">
          <img key={gifKey} src={`/snapchat1.gif?${gifKey}`} alt="WhatsApp" className="w-[41rem] h-[41rem] object-contain translate-x-[-3cm]" />
          <div className="fixed w-[28rem]" style={{ top: "calc(50% - 1cm)", right: "6%" }}>
            <div className="p-4 rounded-[20px] text-2xl border-4 border-cyan-400 shadow-xl"
              style={{
                background: "linear-gradient(180deg, #a0f0f9 0%, #b8f6e9 90%, #c2fbd7 100%)",
                backdropFilter: "blur(4px)",
              }}>
              <p style={{ color: textColor, fontWeight: 'bold' }}>{currentText}</p>
            </div>
            <div className="p-4 rounded-[20px] text-lg border-4 shadow-xl absolute"
              style={{
                top: "5cm",
                marginTop: "-4cm",
                transform: "translateY(4cm)",
                width: "fit-content",
                maxWidth: "100%",
                background: "white",
                border: "3px solid #C2E764",
              }}>
              <p className="text-black font-medium" dangerouslySetInnerHTML={{ __html: secondaryText }} />
            </div>
          </div>
        </div>
      )}

      {/* Teleport Bubble */}
      <TeleportBubble onClick={handleTeleportToNext} color="blue" position="right" text='3.Voices'/>
      <TeleportBubble onClick={handleTeleportToBack} color="purple" position="left" text='Back'/>
    </div>
  );
}

export default SocialMediaQuestion;