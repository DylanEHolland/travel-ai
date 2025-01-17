"use client";

import { ChatMessage } from "@/types/chat";
import { useMutation } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { connectToBackend } from "../helpers/requests";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

export const ChatWindow: React.FC<{ destinationId: string }> = ({
  destinationId,
}) => {
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);

  return (
    <div>
      <ChatHistory chatHistory={chatHistory} />
      <ChatInput
        pushResponse={(response) => setChatHistory([...chatHistory, response])}
        destinationId={destinationId}
      />
    </div>
  );
};

export const ChatHistory = ({
  chatHistory,
}: {
  chatHistory: ChatMessage[];
}) => {
  console.log("chatHistory", chatHistory);
  return (
    <div>
      {chatHistory.map((message, index) => {
        console.log(message);
        return <div key={index}>{message}</div>;
      })}
    </div>
  );
};

export const ChatInput = ({
  pushResponse,
  destinationId,
}: {
  pushResponse: (response: ChatMessage) => void;
  destinationId: string;
}) => {
  const { register, handleSubmit } = useForm<ChatMessage>();

  const { mutate: sendChat } = useMutation({
    mutationFn: (data: ChatMessage) => {
      return connectToBackend("/chat", "POST", {
        message: data.message,
        destinationId,
      });
    },
    onMutate: () => {},
    onSuccess: (data) => {
      console.log(data);
      pushResponse(data.response);
    },
    onError: () => {},
    onSettled: () => {
      //   refetch();
    },
  });

  const onSubmit = (data: ChatMessage) => {
    sendChat(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <Textarea
          {...register("message")}
          style={{
            width: "500px",
            height: "100px",
            border: "1px solid #111",
            padding: "10px",
            resize: "none",
          }}
        />
      </div>
      <Button type="submit">Send</Button>
    </form>
  );
};
