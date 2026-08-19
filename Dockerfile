FROM node:22-bookworm-slim

WORKDIR /app

COPY integrations/mcp-ai-hive-aigc/package.json integrations/mcp-ai-hive-aigc/package-lock.json ./
RUN npm ci --omit=dev

COPY integrations/mcp-ai-hive-aigc/src ./src
COPY integrations/mcp-ai-hive-aigc/.well-known ./.well-known

ENV NODE_ENV=production
ENV HOST=0.0.0.0
ENV PORT=3000

EXPOSE 3000

CMD ["node", "src/index.js"]
