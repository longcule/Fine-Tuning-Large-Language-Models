export const DEFAULT_SYSTEM_PROMPT =
  process.env.NEXT_PUBLIC_DEFAULT_SYSTEM_PROMPT ||
  "Bạn là một trợ lý đáng tin cậy, hãy sử dụng những gì bạn biết để trả lời câu hỏi sau đây. Nếu bạn không biết, cứ nói là không biết."

export const OPENAI_API_HOST =
  process.env.OPENAI_API_HOST || 'https://fe5d-34-142-131-6.ngrok-free.app';

export const DEFAULT_TEMPERATURE = 
  parseFloat(process.env.NEXT_PUBLIC_DEFAULT_TEMPERATURE || "1");

export const OPENAI_API_TYPE =
  process.env.OPENAI_API_TYPE || 'openai';

export const OPENAI_API_VERSION =
  process.env.OPENAI_API_VERSION || '2023-03-15-preview';

export const OPENAI_ORGANIZATION =
  process.env.OPENAI_ORGANIZATION || '';

export const AZURE_DEPLOYMENT_ID =
  process.env.AZURE_DEPLOYMENT_ID || '';
