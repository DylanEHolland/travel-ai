"use client";

import { ChatWindow } from "@/lib/components/Chat";
import { useParams } from "next/navigation";

const Chat = () => {
  const { destinationId } = useParams();
  return <ChatWindow destinationId={destinationId as string} />;
};

export default Chat;
