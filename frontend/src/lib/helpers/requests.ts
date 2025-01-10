import { config } from "dotenv";
config();

export const connectToBackend = async <T>(
  path: string,
  method: "GET" | "POST" | "PUT" | "DELETE" = "GET",
  body?: T
) => {
  if (!process.env.BACKEND_URL) {
    throw new Error("BACKEND_URL is not set");
  }

  const options: RequestInit = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (body) {
    options.body = JSON.stringify(body);
  }

  const response = await fetch(`${process.env.BACKEND_URL}${path}`, options);
  if (!response.ok) {
    throw new Error("Failed to connect to backend");
  }

  return response.json();
};
