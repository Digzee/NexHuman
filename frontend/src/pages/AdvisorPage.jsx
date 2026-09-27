import { useState } from "react";

import { API_BASE_URL } from "../config/api";
import { useAuth } from "../context/AuthContext";


const STARTER_QUESTIONS = [
  "Explain my latest optimisation result.",
  "Why did the optimiser favour BTC and ETH?",
  "How does the GA result compare with equal weighting?",
  "What does my Sharpe ratio mean?",
];


function AdvisorPage() {
  const { authenticatedFetch } = useAuth();

  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");


  async function sendMessage(question) {
    const trimmedMessage = question.trim();

    if (!trimmedMessage || isLoading) {
      return;
    }

    const userMessage = {
      role: "user",
      content: trimmedMessage,
    };

    setMessages((current) => [
      ...current,
      userMessage,
    ]);

    setMessage("");
    setError("");
    setIsLoading(true);

    try {
      const response = await authenticatedFetch(
        `${API_BASE_URL}/advisor/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: trimmedMessage,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            "The AI advisor could not respond."
        );
      }

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: data.answer,
        },
      ]);
    } catch (requestError) {
      setError(
        requestError.message ||
          "The AI advisor is temporarily unavailable."
      );
    } finally {
      setIsLoading(false);
    }
  }


  function handleSubmit(event) {
    event.preventDefault();
    sendMessage(message);
  }


  return (
    <section className="pb-12">
      <p className="text-sm font-medium text-cyan-400">
        AI Advisor
      </p>

      <h1 className="mt-2 text-3xl font-semibold tracking-tight text-white sm:text-4xl">
        Understand your portfolio
      </h1>

      <p className="mt-3 max-w-3xl text-sm leading-6 text-slate-400">
        Ask NexHuman about your investor profile,
        portfolio holdings and latest genetic algorithm
        optimisation result.
      </p>


      <div className="mt-8 grid gap-5 xl:grid-cols-[1fr_300px]">
        <div className="overflow-hidden rounded-2xl border border-white/10 bg-[#0B1020]">
          <div className="border-b border-white/10 px-6 py-4">
            <div className="flex items-center gap-3">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-gradient-to-br from-violet-600 to-cyan-500 text-sm font-bold text-white">
                N
              </div>

              <div>
                <p className="text-sm font-semibold text-white">
                  NexHuman Advisor
                </p>

                <p className="text-xs text-slate-500">
                  Portfolio-aware AI assistant
                </p>
              </div>
            </div>
          </div>


          <div className="min-h-[420px] space-y-5 p-6">
            {messages.length === 0 && (
              <div className="mx-auto max-w-xl py-12 text-center">
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-600/20 to-cyan-400/20 text-xl font-semibold text-cyan-300">
                  N
                </div>

                <h2 className="mt-5 text-xl font-semibold text-white">
                  Ask about your NexHuman results
                </h2>

                <p className="mt-2 text-sm leading-6 text-slate-400">
                  I can explain your optimisation,
                  investor profile, portfolio and
                  risk metrics using your NexHuman
                  data.
                </p>
              </div>
            )}


            {messages.map((chatMessage, index) => (
              <Message
                key={`${chatMessage.role}-${index}`}
                role={chatMessage.role}
                content={chatMessage.content}
              />
            ))}


            {isLoading && (
              <div className="flex justify-start">
                <div className="max-w-[85%] rounded-2xl rounded-tl-sm bg-white/[0.05] px-4 py-3">
                  <p className="text-sm text-slate-400">
                    NexHuman is analysing your data...
                  </p>
                </div>
              </div>
            )}


            {error && (
              <p
                role="alert"
                className="rounded-xl border border-red-400/20 bg-red-400/[0.05] px-4 py-3 text-sm text-red-300"
              >
                {error}
              </p>
            )}
          </div>


          <form
            onSubmit={handleSubmit}
            className="border-t border-white/10 p-4"
          >
            <div className="flex gap-3">
              <input
                type="text"
                value={message}
                onChange={(event) =>
                  setMessage(event.target.value)
                }
                placeholder="Ask about your portfolio..."
                maxLength={2000}
                disabled={isLoading}
                className="min-w-0 flex-1 rounded-xl border border-white/10 bg-[#11172A] px-4 py-3 text-sm text-white outline-none placeholder:text-slate-600 focus:border-cyan-400 disabled:opacity-60"
              />

              <button
                type="submit"
                disabled={
                  isLoading ||
                  !message.trim()
                }
                className="rounded-xl bg-gradient-to-r from-violet-600 to-blue-600 px-5 py-3 text-sm font-semibold text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
              >
                Send
              </button>
            </div>

            <p className="mt-3 text-xs leading-5 text-slate-600">
              NexHuman provides educational
              decision-support information, not
              financial advice.
            </p>
          </form>
        </div>


        <aside className="space-y-5">
          <div className="rounded-2xl border border-white/10 bg-[#0B1020] p-5">
            <p className="text-xs font-medium uppercase tracking-[0.18em] text-slate-500">
              Suggested questions
            </p>

            <div className="mt-4 space-y-2">
              {STARTER_QUESTIONS.map(
                (question) => (
                  <button
                    key={question}
                    type="button"
                    disabled={isLoading}
                    onClick={() =>
                      sendMessage(question)
                    }
                    className="w-full rounded-xl border border-white/5 bg-white/[0.02] px-4 py-3 text-left text-sm leading-5 text-slate-300 transition hover:border-cyan-400/30 hover:bg-cyan-400/[0.03] disabled:opacity-50"
                  >
                    {question}
                  </button>
                )
              )}
            </div>
          </div>


          <div className="rounded-2xl border border-cyan-400/10 bg-cyan-400/[0.02] p-5">
            <p className="text-sm font-semibold text-white">
              Context-aware
            </p>

            <p className="mt-2 text-xs leading-5 text-slate-400">
              The advisor receives your investor
              profile, current portfolio information
              and latest saved optimisation result as
              context for each question.
            </p>
          </div>
        </aside>
      </div>
    </section>
  );
}


function Message({
  role,
  content,
}) {
  const isUser = role === "user";

  return (
    <div
      className={`flex ${
        isUser
          ? "justify-end"
          : "justify-start"
      }`}
    >
      <div
        className={`max-w-[85%] whitespace-pre-wrap rounded-2xl px-4 py-3 text-sm leading-6 ${
          isUser
            ? "rounded-tr-sm bg-gradient-to-r from-violet-600 to-blue-600 text-white"
            : "rounded-tl-sm bg-white/[0.05] text-slate-300"
        }`}
      >
        {content}
      </div>
    </div>
  );
}


export default AdvisorPage;