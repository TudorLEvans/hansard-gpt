"use client";
import { useState, useCallback, useRef, useEffect } from "react";
import styles from "./form.module.css";
import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

type InputFormProps = {
  onSubmit: (query: string) => void;
};

export default function InputForm({ onSubmit }: InputFormProps) {
  const [query, setQuery] = useState<string>("");
  const [wordCount, setWordCount] = useState<number>(0);

  const formRef = useRef<HTMLFormElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const onEnterPress = useCallback((e: KeyboardEvent) => {
    if (e.keyCode == 13 && e.shiftKey == false) {
      e.preventDefault();
      if (formRef.current) formRef.current.requestSubmit();
    }
  }, []);

  function handleResize() {
    if (!textareaRef.current) return;
    textareaRef.current.style.height = "0px";
    const computed = window.getComputedStyle(textareaRef.current);
    const height =
      parseInt(computed.getPropertyValue("border-top-width")) +
      textareaRef.current.scrollHeight +
      parseInt(computed.getPropertyValue("border-bottom-width"));

    textareaRef.current.style.height = `${height}px`;
  }

  useEffect(() => {
    handleResize();
    if (query == "") setWordCount(0);
    else setWordCount(query.split(" ").length);
  }, [query]);

  return (
    <form
      ref={formRef}
      className={styles.form}
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit?.(query);
        setQuery("");
      }}
    >
      <textarea
        ref={textareaRef}
        onKeyDown={(e) => {
          onEnterPress(e as any);
        }}
        className={`${styles.textarea} ${inter.className}`}
        value={query}
        placeholder="Ask me anything"
        onChange={(e) => {
          e.preventDefault();
          if (e.target.value.split(" ").length <= 400) setQuery(e.target.value);
        }}
      />
      <div className={styles.subtext}>
        <p>{wordCount} / 400</p>
      </div>
    </form>
  );
}
