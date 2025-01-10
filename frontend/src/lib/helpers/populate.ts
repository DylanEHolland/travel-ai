import { QueryClient } from "@tanstack/react-query";
import { connectToBackend } from "./requests";
import { Destination } from "@/types/destination";

export const syncObjectToStore = async <T>(
  client: QueryClient,
  key: string,
  data: (T & { id: string }) | (T & { id: string })[]
) => {
  if (Array.isArray(data)) {
    for (const item of data) {
      syncObjectToStore(client, key, item);
    }
  } else {
    client.setQueryData([key, data.id], data);
  }
};

export const populateDestinations = async (client: QueryClient) => {
  const response = await connectToBackend("/destinations", "GET");

  return new Promise((resolve) => {
    client.setQueryData(
      ["destinations"],
      response.destinations.map((d: { id: string }) => d.id)
    );
    syncObjectToStore<Destination>(
      client,
      "destinations",
      response.destinations[0]
    );
    resolve(null);
  });
};
