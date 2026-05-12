FROM node:22-slim AS builder
WORKDIR /usr/src/app
COPY package.json package-lock.json* ./
RUN npm ci

FROM node:22-slim
WORKDIR /usr/src/app

# Quartz-Engine und Konfiguration
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY quartz/ ./quartz/
COPY quartz.config.ts quartz.layout.ts tsconfig.json globals.d.ts index.d.ts ./

# content/ wird via docker-compose als Volume gemountet (live-reload)
# attachments/ wird ebenfalls gemountet

EXPOSE 8080
CMD ["npx", "quartz", "build", "--serve", "--port", "8080", "--host", "0.0.0.0"]
