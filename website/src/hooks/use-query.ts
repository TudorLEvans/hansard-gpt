"use client";
import { useState, useCallback } from "react";

export type Answer = {
  answer: string;
  sources: any;
};

export default function useQuery() {
  const [loading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error>();

  const getAnswer = useCallback(
    async (query: string) => {
      try {
        setError(undefined)
        setIsLoading(true);
        const res = await fetch("http://localhost:8000/answers", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question: query,
          }),
        });
        if (!res.ok) {
          throw new Error("Failed to fetch data");
        }
        return res.json();
      } catch (error) {
        setError(error as Error);
      } finally {
        setIsLoading(false);
      }
    },
    [loading, setIsLoading, error, setError]
  );

  return {
    loading,
    error,
    getAnswer,
  };
}
