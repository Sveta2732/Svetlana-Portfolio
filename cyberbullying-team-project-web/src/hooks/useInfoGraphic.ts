import { useState, useRef } from 'react';
import { IconData, InfographicState, InfographicViewModel } from '../types/infographic.types';
import { v4 as uuidv4 } from 'uuid';

/**
 * @function useInfographicViewModel
 * @description
 * ViewModel for the Infographic component following MVVM pattern.
 * Handles all business logic and data processing for the infographic visualization.
 *
 * @returns {InfographicViewModel} State and methods for the infographic component
 */
export const useInfographicViewModel = (): InfographicViewModel => {
  // Main state for the infographic
  const [state, setState] = useState<InfographicState>({
    studentCount: 0,
    showCaptions: false,
    icons: [],
    isAnimating: false,
    currentStep: 0,
  });

  // References with correct typing
  const audioRef = useRef<HTMLAudioElement>(null);
  const gridRef = useRef<HTMLDivElement>(null);

  /**
   * @function sleep
   * @description Creates a promise that resolves after a specified delay
   * @param {number} ms - Milliseconds to delay
   * @returns {Promise<void>}
   */
  const sleep = (ms: number): Promise<void> => {
    return new Promise(resolve => setTimeout(resolve, ms));
  };

  /**
   * @function createIconData
   * @description Creates icon data object with specified properties
   * @param {string} gender - Gender of the icon ('boy' or 'girl')
   * @param {'normal' | 'orange' | 'maroon'} state - Visual state of the icon
   * @returns {IconData} Created icon data
   */
  const createIconData = (gender: 'boy' | 'girl', state: 'normal' | 'orange' | 'maroon' = 'normal'): IconData => {
    return {
      id: uuidv4(),
      gender,
      state,
      highlighted: false,
    };
  };

  /**
   * @function handleStudentCountChange
   * @description Updates the student count in the state
   * @param {number} count - New student count value
   */
  const handleStudentCountChange = (count: number): void => {
    setState(prev => ({
      ...prev,
      studentCount: count
    }));
  };

  /**
   * @function calculateIconSize
   * @description Calculates the optimal icon size based on student count
   * @param {number} count - Number of students
   * @returns {number} Icon size in pixels
   */
  const calculateIconSize = (count: number): number => {
    return Math.max(24, 60 - (count - 10) * 0.2);
  };

  /**
   * @function generateIcons
   * @description Generates the initial set of icons based on student count
   * @param {number} count - Number of students to generate
   */
  const generateIcons = (count: number): void => {
    if (isNaN(count) || count < 10 || count > 200) {
      alert("Enter a number between 10 and 200");
      return;
    }

    // Generate icons (half boys, half girls)
    const newIcons: IconData[] = [];
    for (let i = 0; i < count; i++) {
      const gender = Math.random() < 0.5 ? 'boy' : 'girl';
      newIcons.push(createIconData(gender));
    }

    setState(prev => ({
      ...prev,
      studentCount: count,
      showCaptions: true,
      icons: newIcons,
      isAnimating: true,
      currentStep: 0
    }));

    // Start the animation sequence
    animateInfographic(newIcons, count);
  };

  /**
   * @function animateInfographic
   * @description Main animation sequence that updates icons and shows captions
   * @param {IconData[]} initialIcons - Initial set of icons
   * @param {number} count - Total number of students
   */
  const animateInfographic = async (initialIcons: IconData[], count: number): Promise<void> => {
    // Step 1: Identify victims (30%): 60% girls, 40% boys
    const bulliedCount = Math.ceil(count * 0.3);
    const numGirls = Math.round(bulliedCount * 0.6);
    const numBoys = bulliedCount - numGirls;
    
    // Create separate arrays for boys and girls
    const girlIndices: number[] = [];
    const boyIndices: number[] = [];
    
    initialIcons.forEach((icon, index) => {
      if (icon.gender === 'girl') {
        girlIndices.push(index);
      } else {
        boyIndices.push(index);
      }
    });
    
    // Shuffle arrays to ensure random selection
    girlIndices.sort(() => Math.random() - 0.5);
    boyIndices.sort(() => Math.random() - 0.5);
    
    // Select victims
    const selectedGirlIndices = girlIndices.slice(0, numGirls);
    const selectedBoyIndices = boyIndices.slice(0, numBoys);
    const selectedIndices = [...selectedGirlIndices, ...selectedBoyIndices];
    
    // Shuffle the victim indices to randomize the order of highlighting
    selectedIndices.sort(() => Math.random() - 0.5);
    
    // Start with all initial icons
    let updatedIcons = [...initialIcons];
    
    // Highlight victims one by one
    for (let i = 0; i < selectedIndices.length; i++) {
      const idx = selectedIndices[i];
      
      await sleep(100 + Math.random() * 100);
      
      // Update state to 'orange'
      updatedIcons = updatedIcons.map((icon, index) => 
        index === idx ? { ...icon, state: 'orange' } : icon
      );
      
      // Play sound
      if (audioRef.current) {
        audioRef.current.currentTime = 0;
        audioRef.current.volume = 1;
        try {
          await audioRef.current.play();
        } catch (e) {
          console.error("Audio play error:", e);
        }
      }
      
      // Update state
      setState(prev => ({
        ...prev,
        icons: updatedIcons,
        currentStep: 1
      }));
    }
    
    // Wait for first caption to be read
    await sleep(2000);
    
    // Step 2: Highlight girls among victims
    setState(prev => ({
      ...prev,
      currentStep: 2,
    }));
    
    // Highlight only girls who were selected as victims
    const victimGirlIndices = selectedIndices.filter(idx => 
      updatedIcons[idx].gender === 'girl' && updatedIcons[idx].state === 'orange'
    );
    
    // Apply highlight to victim girls
    updatedIcons = updatedIcons.map((icon, index) => 
      victimGirlIndices.includes(index) ? { ...icon, highlighted: true } : icon
    );
    
    setState(prev => ({
      ...prev,
      icons: updatedIcons
    }));
    
    await sleep(3000);
    
    // Remove highlighting
    updatedIcons = updatedIcons.map(icon => ({ ...icon, highlighted: false }));
    
    setState(prev => ({
      ...prev,
      icons: updatedIcons
    }));
    
    // Step 3: Highlight those who disclosed (20% of victims)
    setState(prev => ({
      ...prev,
      currentStep: 3
    }));
    
    // Select 20% of victims to disclose (randomly)
    let orangeIndices = selectedIndices.filter(idx => updatedIcons[idx].state === 'orange');
    // Shuffle to select random victims
    orangeIndices.sort(() => Math.random() - 0.5);
    const disclosedCount = Math.max(1, Math.round(orangeIndices.length * 0.2));
    orangeIndices = orangeIndices.slice(0, disclosedCount);
    
    // Update disclosed victims to maroon one by one
    for (let i = 0; i < orangeIndices.length; i++) {
      const idx = orangeIndices[i];
      
      await sleep(100 + Math.random() * 100);
      
      // Update to maroon state
      updatedIcons = updatedIcons.map((icon, index) => 
        index === idx ? { ...icon, state: 'maroon' } : icon
      );
      
      // Play sound
      if (audioRef.current) {
        audioRef.current.currentTime = 0;
        audioRef.current.volume = 1;
        try {
          await audioRef.current.play();
        } catch (e) {
          console.error("Audio play error:", e);
        }
      }
      
      // Update state
      setState(prev => ({
        ...prev,
        icons: updatedIcons
      }));
    }
    
    // Final captions
    await sleep(4000);
    setState(prev => ({ ...prev, currentStep: 4 }));
    
    await sleep(3000);
    setState(prev => ({ ...prev, currentStep: 5 }));
    
    await sleep(3000);
    setState(prev => ({ ...prev, isAnimating: false }));
  };

  /**
   * @function getIconSrc
   * @description Gets the image source for an icon based on gender and state
   * @param {string} gender - Gender of the icon ('boy' or 'girl')
   * @param {string} state - Visual state of the icon
   * @returns {string} Path to the icon image
   */
  const getIconSrc = (gender: 'boy' | 'girl', state: 'normal' | 'orange' | 'maroon') => {
    const basePath = '/quizPage';
  
    if (gender === 'boy') {
      if (state === 'normal') return `${basePath}/boy.svg`;
      if (state === 'orange') return `${basePath}/boy_orange.svg`;
      if (state === 'maroon') return `${basePath}/boy_maroon.svg`;
    } else {
      if (state === 'normal') return `${basePath}/girl.svg`;
      if (state === 'orange') return `${basePath}/girl_orange.svg`;
      if (state === 'maroon') return `${basePath}/girl_maroon.svg`;
    }
  
    return '';
  };

  /**
   * @function resetInfographic
   * @description Resets the infographic to its initial state
   */
  const resetInfographic = (): void => {
    setState({
      studentCount: 0,
      showCaptions: false,
      icons: [],
      isAnimating: false,
      currentStep: 0,
    });
  };

  return {
    state,
    audioRef: audioRef as React.RefObject<HTMLAudioElement>,
    gridRef: gridRef as React.RefObject<HTMLDivElement>,
    handleStudentCountChange,
    generateIcons,
    resetInfographic,
    getIconSrc,
    calculateIconSize,
  };
};