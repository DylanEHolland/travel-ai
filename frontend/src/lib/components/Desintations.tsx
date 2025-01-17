import { useMutation, useQuery } from "@tanstack/react-query";
import { connectToBackend } from "../helpers/requests";
import { useForm } from "react-hook-form";
import { Destination, NewDestination } from "@/types/destination";
import Link from "next/link";
import { useDestination } from "../hooks/useDestination";
import { KnowledgeBase } from "./KnowledgeBase";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export const Destinations = () => {
  const { data: destinations, refetch } = useQuery({
    queryKey: ["destinations"],
    queryFn: async () => {
      const result = await connectToBackend("/destinations", "GET");
      return result.destinations;
    },
  });

  return (
    <div>
      <NewDestinationForm refetch={refetch} />
      <br />
      <ol>
        {destinations?.map((destination: Destination) => (
          <li key={destination.id}>
            <Link href={`/destinations/${destination.id}`}>
              {destination.name}
            </Link>
          </li>
        ))}
      </ol>
    </div>
  );
};

export const NewDestinationForm = ({ refetch }: { refetch: () => void }) => {
  const { mutate: createDestination } = useMutation({
    mutationFn: (data: NewDestination) => {
      return connectToBackend("/destinations", "POST", data);
    },
    onMutate: () => {},
    onSuccess: () => {},
    onError: () => {},
    onSettled: () => {
      refetch();
    },
  });

  const { register, handleSubmit } = useForm<NewDestination>();

  const onSubmit = (data: NewDestination) => {
    createDestination(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div className="flex flex-row gap-2">
        <Input {...register("name")} placeholder="Add new destination" />
        <Button type="submit">Save</Button>
      </div>
    </form>
  );
};

export const DestinationDetails = ({
  destinationId,
}: {
  destinationId: string;
}) => {
  const destination = useDestination(destinationId);
  return (
    <div>
      <div>{destination?.name}</div>
      <hr />
      <br />
      <Link href={`/destinations/${destinationId}/chat`}>
        <Button>Chat</Button>
      </Link>
      <br />
      <br />
      <KnowledgeBase destinationId={destinationId} />
    </div>
  );
};
