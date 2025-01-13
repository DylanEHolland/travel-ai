"use client";

import { DestinationDetails } from "@/lib/components/Desintations";
import { useParams } from "next/navigation";

const DestinationPage = () => {
  const { destinationId } = useParams<{ destinationId: string }>();
  return <DestinationDetails destinationId={destinationId} />;
};

export default DestinationPage;
