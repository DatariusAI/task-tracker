import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic(); // reads ANTHROPIC_API_KEY from env

export const chat = async (req, res) => {
  try {
    const { message } = req.body;

    if (!message) {
      return res.status(400).json({ error: "message is required" });
    }

    const response = await client.messages.create({
      model: "claude-sonnet-4-5",
      max_tokens: 1024,
      messages: [{ role: "user", content: message }],
    });

    res.json({ reply: response.content[0].text });
  } catch (err) {
    console.error("Claude API error:", err);
    res.status(500).json({ error: "Claude API call failed" });
  }
};
