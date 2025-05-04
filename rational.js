// Advanced human-like response timing for therapy rational chatbot
// This function adds context-aware delays based on question complexity
// For use in Flowise JS Function node - stay tune with Pejman :)
// written by Pejman - 31.03.2025

// PART 2-rational: BACKEND - JS FUNCTION NODE

const config = {
  baseReadingTime: 1500,
  msPerCharacter: 20,
  minimumResponseTime: 2000,
  randomVariation: 500,
};

function addRandomVariation(baseTime) {
  const variation = Math.floor(Math.random() * config.randomVariation);
  return baseTime + variation;
}

function calculateResponseDelay(text) {
  const readingTime = addRandomVariation(config.baseReadingTime);
  const typingTime = Math.max(
    text.length * config.msPerCharacter,
    config.minimumResponseTime
  );

  // Total delay
  return readingTime + typingTime;
}

// Handle FLOWISE_NEWLINE removal
function cleanResponse(text) {
  if (!text || typeof text !== "string") return text;

  const cleanedText = text.replace(/FLOWISE_NEWLINE/g, " ");

  return cleanedText.replace(/\s+/g, " ").trim();
}

async function process() {
  let botResponse = $flow.rawOutput;

  if (!botResponse || typeof botResponse !== "string") {
    return botResponse;
  }

  botResponse = cleanResponse(botResponse);

  // Calculate total delay
  const totalDelay = calculateResponseDelay(botResponse);

  console.log(`Response length: ${botResponse.length} characters`);
  console.log(`Total delay: ${totalDelay}ms (${totalDelay / 1000} seconds)`);

  await new Promise((resolve) => setTimeout(resolve, totalDelay));

  return botResponse;
}

return process();
