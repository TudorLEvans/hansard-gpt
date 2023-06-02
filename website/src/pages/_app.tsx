import "./globals.css";
import { Inter } from "next/font/google";
import Head from "next/head";
import Header from "@/components/header";
import styles from "./page.module.css";
import type { NextPage } from 'next';
import type { AppProps } from 'next/app';

const inter = Inter({ subsets: ["latin"] });

function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Head>
        <title>Commons GPT</title>
        <meta
          property="description"
          content="Search through Hansard with the help of the latest AI technology"
          key="description"
        />
      </Head>

      <div className={inter.className + " base"}>
        <main className={styles.main}>
          <Header />
          {children}
        </main>
      </div>
    </>
  );
}

type AppPropsWithLayout = AppProps & {
    Component: NextPage;
  };

export default function MyApp({ Component, pageProps }: AppPropsWithLayout) {
  return (
    <RootLayout>
      <Component {...pageProps} />
    </RootLayout>
  );
}
