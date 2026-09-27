import { useEffect, useState } from "react";

import InvestorProfileQuestionnaire from "../components/profiling/InvestorProfileQuestionnaire";
import { API_BASE_URL } from "../config/api";
import { useAuth } from "../context/AuthContext";


const EMPTY_ANSWERS = {
  investment_horizon: null,
  loss_tolerance: null,
  volatility_comfort: null,
  investment_experience: null,
  growth_preference: null,
};


function InvestorProfilePage() {
  const { authenticatedFetch } = useAuth();

  const [answers, setAnswers] =
    useState(EMPTY_ANSWERS);

  const [profile, setProfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] =
    useState(false);
  const [error, setError] = useState("");


  useEffect(() => {
    async function fetchProfile() {
      try {
        const response = await authenticatedFetch(
          `${API_BASE_URL}/profiling/`
        );

        if (response.status === 404) {
          return;
        }

        if (!response.ok) {
          throw new Error();
        }

        const data = await response.json();

        setProfile(data);

        setAnswers({
          investment_horizon:
            data.investment_horizon,
          loss_tolerance:
            data.loss_tolerance,
          volatility_comfort:
            data.volatility_comfort,
          investment_experience:
            data.investment_experience,
          growth_preference:
            data.growth_preference,
        });
      } catch {
        setError(
          "We couldn't load your investor profile."
        );
      } finally {
        setIsLoading(false);
      }
    }

    fetchProfile();

    // authenticatedFetch is provided by AuthContext.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


  function handleAnswerChange(
    field,
    value
  ) {
    setAnswers((currentAnswers) => ({
      ...currentAnswers,
      [field]: value,
    }));

    setError("");
  }


  async function handleSubmit(event) {
    event.preventDefault();

    const hasMissingAnswer =
      Object.values(answers).some(
        (value) => value === null
      );

    if (hasMissingAnswer) {
      setError(
        "Please answer all five questions."
      );

      return;
    }

    setError("");
    setIsSubmitting(true);

    try {
      const response = await authenticatedFetch(
        `${API_BASE_URL}/profiling/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(answers),
        }
      );

      if (!response.ok) {
        throw new Error();
      }

      const data = await response.json();

      setProfile(data);
    } catch {
      setError(
        "We couldn't calculate your investor profile. Please try again."
      );
    } finally {
      setIsSubmitting(false);
    }
  }


  if (isLoading) {
    return (
      <section>
        <p className="text-sm text-slate-400">
          Loading investor profile...
        </p>
      </section>
    );
  }


  return (
    <section>
      <p className="text-sm font-medium text-cyan-400">
        Investor Profile
      </p>

      <h1 className="mt-2 text-3xl font-semibold tracking-tight text-white sm:text-4xl">
        Understand your risk tolerance
      </h1>

      <p className="mt-3 max-w-2xl text-sm leading-6 text-slate-400">
        Answer five questions to help NexHuman understand
        your investment preferences. Your profile will later
        help guide portfolio optimisation and explanations.
      </p>


      {profile && (
        <div className="mt-8 rounded-2xl border border-cyan-400/20 bg-cyan-400/[0.04] p-6">
          <p className="text-xs font-medium uppercase tracking-[0.18em] text-cyan-400">
            Your investor profile
          </p>

          <div className="mt-4 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <p className="text-3xl font-semibold text-white">
                {profile.risk_label_display}
              </p>

              <p className="mt-2 text-sm text-slate-400">
                Risk tolerance
              </p>
            </div>

            <div className="sm:text-right">
              <p className="text-2xl font-semibold text-slate-100">
                {profile.risk_score}/25
              </p>

              <p className="mt-1 text-xs text-slate-500">
                NexHuman profile score
              </p>
            </div>
          </div>

          <p className="mt-5 border-t border-white/10 pt-4 text-xs leading-5 text-slate-500">
            This profile reflects your questionnaire
            responses and is separate from the observed
            risk of any individual portfolio. It is an
            educational indicator, not financial advice.
          </p>
        </div>
      )}


      <InvestorProfileQuestionnaire
        answers={answers}
        onAnswerChange={handleAnswerChange}
        onSubmit={handleSubmit}
        isSubmitting={isSubmitting}
        error={error}
      />
    </section>
  );
}


export default InvestorProfilePage;