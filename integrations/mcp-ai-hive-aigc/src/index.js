import { createMcpExpressApp } from "@modelcontextprotocol/sdk/server/express.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";

import { buildServer } from "./server.js";


const port = Number(process.env.PORT || 3000);
const host = process.env.HOST || "127.0.0.1";
const baseUrl = process.env.AI_HIVE_BASE_URL || "https://ai-hive.iclip.cn/api";
const app = createMcpExpressApp({ host });


function apiKeyFromRequest(request) {
  const direct = request.header("x-ai-hive-api-key");
  if (direct) return direct;
  const authorization = request.header("authorization") || "";
  if (authorization.startsWith("Bearer sk-api-")) return authorization.slice("Bearer ".length);
  return process.env.AI_HIVE_API_KEY || "";
}


app.get("/health", (_request, response) => {
  response.json({ ok: true, service: "ai-hive-aigc-mcp", version: "0.1.0" });
});

app.get("/.well-known/mcp/server-card.json", (_request, response) => {
  response.sendFile("server-card.json", { root: new URL("../.well-known", import.meta.url).pathname });
});

app.post("/mcp", async (request, response) => {
  const server = buildServer({ apiKey: apiKeyFromRequest(request), baseUrl });
  const transport = new StreamableHTTPServerTransport({
    sessionIdGenerator: undefined,
    enableJsonResponse: true,
  });
  try {
    await server.connect(transport);
    await transport.handleRequest(request, response, request.body);
  } catch (error) {
    console.error("MCP request failed", error);
    if (!response.headersSent) {
      response.status(500).json({
        jsonrpc: "2.0",
        error: { code: -32603, message: "Internal server error" },
        id: null,
      });
    }
  } finally {
    await transport.close();
    await server.close();
  }
});

for (const method of ["get", "delete"]) {
  app[method]("/mcp", (_request, response) => {
    response.status(405).json({
      jsonrpc: "2.0",
      error: { code: -32000, message: "Method not allowed" },
      id: null,
    });
  });
}

const httpServer = app.listen(port, host, (error) => {
  if (error) {
    console.error("Failed to start AI Hive MCP server", error);
    process.exit(1);
  }
  console.log(`AI Hive MCP server listening on http://${host}:${port}/mcp`);
});

process.on("SIGINT", () => httpServer.close(() => process.exit(0)));
process.on("SIGTERM", () => httpServer.close(() => process.exit(0)));
