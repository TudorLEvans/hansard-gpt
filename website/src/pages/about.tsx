"use client";

export default function About() {
  return (
    <>
      <h1>Welcome to Common GPT</h1>
      <p>A Tudor Evans Proof of Concept</p>
      <div>
        <p>
          Commons GPT is proof of concept attempt to provide a simple search
          interface for querying the UK government&apos;s Hansard transcripts. These
          transcripts constitute a near universal record of what is said in the
          Houses of Parliamentary. It&apos;s a lot of data! And it&apos;s not so easy to
          find specific information from within that data.
        </p>
        <p>
          By bringing together the open source sBERT SentenceTransformers for
          text embedding, and OpenAI&apos;s ChatGPT API, I&apos;ve attempted to provide a
          neat way of both searching for relevant information within Hansard,
          and digesting that information into an easy-to-read summary that helps
          with information comprehension.
        </p>
        <p>
          A few points of admin. First, some of these servers are expensive to
          run! If you have any issues, it might be because I&apos;m trying to
          minimise compute and expenditure on OpenAI&apos;s API. Second, I have no
          affiliation with Hansard or the UK government. All the data used
          within this app is shared with the Open Government license and
          therefore free for anyone to use in any way in perpetuity. I&apos;m aware
          that gaining mass amounts of Hansard data is hard (I had to write web
          scrapers to do it) so if you would like the raw data for whatever
          reason, I might be able to help. Finally, ChatGPT is one crazy guy and
          I take no responsibility for what is says. I have made a best
          reasonable effort to check that it doesn&apos;t make any bad, wrong or
          plain weird claims but this cannot be entirely ruled out. Anything it
          says should be cross-referenced with reliable sources, which is why
          I&apos;ve provided links to the original data in the sources section.
        </p>
        <p>
          Finally, <strong>if you have any feedback</strong> then I&apos;d love to
          hear it. The easiest places to reach me if you don&apos;t already have my
          contact details would be{" "}
          <a href="https://www.linkedin.com/in/tudor-evans-5a2232151/">
            LinkedIn
          </a> or <a href="https://github.com/TudorLEvans">GitHub</a>.
        </p>
      </div>
    </>
  );
}
