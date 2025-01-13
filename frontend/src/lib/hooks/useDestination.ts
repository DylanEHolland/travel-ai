import { useQuery } from "@tanstack/react-query";
import { connectToBackend } from "../helpers/requests";

export const useDestination = (destinationId: string) => {
  const { data: destination } = useQuery({
    queryKey: ["destination", destinationId],
    queryFn: async () => {
      const result = await connectToBackend(
        `/destinations/${destinationId}`,
        "GET"
      );
      return result.destination;
    },
  });

  console.log("got data:", destination);
  return destination;
};
