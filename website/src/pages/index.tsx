"use client";
import styles from "./page.module.css";
import InputForm from "@/components/form";
import useQuery from "@/hooks/use-query";
import { useState } from "react";
import Link from "next/link";
import Spinner from "@/components/spinner";

export default function Home() {
  const [query, setQuery] = useState<string>("");
  const [answer, setAnswer] = useState<any>();
  const { error, loading, getAnswer } = useQuery();

  const onSubmit = (query: string) => {
    getAnswer(query)
      .then((res) => {
        setAnswer(res);
        setQuery(query);
      })
      .catch();
  };

  return (
    <>
      <InputForm onSubmit={onSubmit} />
      {loading && <Spinner />}
      {!loading && error && (
        <section>
          <p className={styles.label}>ERROR</p>
          <p>
            Looks like something went wrong - try refreshing the page or
            reaching out to me somehow
          </p>
        </section>
      )}
      {!!answer && !error && !loading && (
        <div className={styles.boxes}>
          <section>
            <p className={styles.label}>QUESTION</p>
            <p>{query}</p>
          </section>
          <section>
            <p className={styles.label}>ANSWER</p>
            {!!answer.answer ? (
              <>
                <p>{answer.answer}</p>
                <p className={styles.label}>
                  This answer was generated using ChatGPT. It's accuracy cannot
                  be guaranteed, so check what it says against the sources
                  listed.
                </p>
              </>
            ) : (
              <p>
                Unable to generate an answer from ChatGPT. This could be due to
                an error, or the monthly credit limit might have been reached
                (you know, running these things is kind of expensive)
              </p>
            )}
          </section>
          {answer?.sources?.map((item: any) => (
            <section>
              <p className={styles.label}>SOURCE</p>
              <p>
                Proceedings from {item.date} -{" "}
                <Link href={item.link}>Read it in Hansard</Link>
              </p>
              <p className={styles.source}><blockquote>{item.text}</blockquote></p>
            </section>
          ))}
        </div>
      )}
    </>
  );
}
