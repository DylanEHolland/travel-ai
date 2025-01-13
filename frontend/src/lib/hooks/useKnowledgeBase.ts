import { useQuery } from "@tanstack/react-query";
import { connectToBackend } from "../helpers/requests";

export const useKnowledgeBase = (destinationId: string) => {
  const { data, isLoading, error } = useQuery({
    queryKey: ["knowledgebase", destinationId],
    queryFn: () => connectToBackend(`/knowledgebase/${destinationId}`, "GET"),
  });

  return { data, isLoading, error };
};
