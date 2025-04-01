// Advanced human-like response timing for therapy empathy chatbot
// This function adds context-aware delays based on question complexity
// For use in Flowise JS Function node - stay tune with Pejman :)
// written by Pejman - 31.03.2025

// PART 1: BACKEND - JS FUNCTION NODE

// Configuration - adjust these values for your preferred timing
const config = {
  // Base time before starting to type (milliseconds)
  baseReadingTime: 3000,
  
  // Time to type per character (milliseconds)
  msPerCharacter: 100,
  
  // Minimum total response time (milliseconds)
  minimumResponseTime: 4000,
  
  // Random variation (milliseconds)
  randomVariation: 1000
};

// Add random variation to timing
function addRandomVariation(baseTime) {
  const variation = Math.floor(Math.random() * config.randomVariation);
  return baseTime + variation;
}

// Calculate total response delay
function calculateResponseDelay(text) {
  // Time to read and think about the question
  const readingTime = addRandomVariation(config.baseReadingTime);
  
  // Time to type the response (based on length)
  const typingTime = Math.max(
    text.length * config.msPerCharacter,
    config.minimumResponseTime
  );
  
  // Total delay
  return readingTime + typingTime;
}

// Handle FLOWISE_NEWLINE removal
function cleanResponse(text) {
  if (!text || typeof text !== 'string') return text;
  
  // Replace all FLOWISE_NEWLINE markers with spaces
  const cleanedText = text.replace(/FLOWISE_NEWLINE/g, ' ');
  
  // Replace multiple spaces with a single space
  return cleanedText.replace(/\s+/g, ' ').trim();
}

// The main function that processes the bot's response
async function process() {
  // Get the raw output from the flow
  let botResponse = $flow.rawOutput;
  
  // Skip process if no valid response
  if (!botResponse || typeof botResponse !== 'string') {
    return botResponse;
  }
  
  // Clean the response of any FLOWISE_NEWLINE markers
  botResponse = cleanResponse(botResponse);
  
  // Calculate total delay
  const totalDelay = calculateResponseDelay(botResponse);
  
  // Log for monitoring (can be removed in production)
  console.log(`Response length: ${botResponse.length} characters`);
  console.log(`Total delay: ${totalDelay}ms (${totalDelay/1000} seconds)`);
  
  // Delay the response to simulate human typing
  await new Promise(resolve => setTimeout(resolve, totalDelay));
  
  // Return the cleaned response
  return botResponse;
}

// Execute the function
return process();