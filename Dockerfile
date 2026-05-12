FROM node:22-slim AS builder
WORKDIR /usr/src/app
COPY package.json package-lock.json* ./
RUN npm ci

FROM node:22-slim
WORKDIR /usr/src/app

COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY package.json ./
COPY quartz/ ./quartz/
COPY quartz.config.ts quartz.layout.ts tsconfig.json globals.d.ts index.d.ts ./

# content/ und attachments/ werden via docker-compose als Volumes gemountet

EXPOSE 8080
CMD ["node", "./quartz/bootstrap-cli.mjs", "build", "--serve", "--port", "8080"]
