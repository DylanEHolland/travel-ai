import { KnowledgeBaseItem, NewKnowledgeBaseItem } from "@/types/knowledgeBase";
import { useForm } from "react-hook-form";
import { connectToBackend } from "../helpers/requests";
import { useMutation } from "@tanstack/react-query";
import { useKnowledgeBase } from "../hooks/useKnowledgeBase";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";

export const KnowledgeBase = ({ destinationId }: { destinationId: string }) => {
  const { data, isLoading, refetch } = useKnowledgeBase(destinationId);

  if (!data || isLoading) return <div>Loading...</div>;
  console.log("got here:", data);
  return (
    <div>
      <CreateKnowledgeBaseItem
        destinationId={destinationId}
        refetch={refetch}
      />
      <br />
      <div>
        {data.knowledgebase.map((item: KnowledgeBaseItem) => (
          <div
            key={item.id}
            className="border border-gray-300 rounded-md p-2"
            style={{ marginBottom: "12px" }}
          >
            {item.text}
          </div>
        ))}
      </div>
    </div>
  );
};

export const CreateKnowledgeBaseItem = ({
  destinationId,
  refetch,
}: {
  destinationId: string;
  refetch: () => void;
}) => {
  const { mutate: createDestination } = useMutation({
    mutationFn: (data: NewKnowledgeBaseItem) => {
      return connectToBackend("/knowledgebase", "POST", {
        ...data,
        destinationId,
      });
    },
    onMutate: () => {},
    onSuccess: () => {},
    onError: () => {},
    onSettled: () => {
      refetch();
    },
  });

  const { register, handleSubmit } = useForm<NewKnowledgeBaseItem>();

  const onSubmit = (data: NewKnowledgeBaseItem) => {
    createDestination(data);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <div>
        <Textarea
          {...register("content")}
          placeholder="Add more content"
          style={{ width: "500px", height: "100px" }}
        />
      </div>
      <Button type="submit">Save</Button>
    </form>
  );
};
