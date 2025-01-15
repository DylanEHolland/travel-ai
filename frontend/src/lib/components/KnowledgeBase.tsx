import { KnowledgeBaseItem, NewKnowledgeBaseItem } from "@/types/knowledgeBase";
import { useForm } from "react-hook-form";
import { connectToBackend } from "../helpers/requests";
import { useMutation } from "@tanstack/react-query";
import { useKnowledgeBase } from "../hooks/useKnowledgeBase";

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
      <div>
        {data.knowledgebase.map((item: KnowledgeBaseItem) => (
          <div key={item.id}>{item.text}</div>
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
        <textarea
          {...register("content")}
          placeholder="Add more content"
          style={{ width: "500px", height: "100px" }}
        />
      </div>
      <button type="submit">Save</button>
    </form>
  );
};
