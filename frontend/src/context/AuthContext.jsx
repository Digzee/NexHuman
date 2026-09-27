import {
  createContext,
  useContext,
  useEffect,
  useState,
} from "react";


const AuthContext = createContext(null);

const API_BASE_URL = "http://127.0.0.1:8000/api/v1";


export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [refreshToken, setRefreshToken] = useState(
    () => sessionStorage.getItem("refreshToken")
  );
  const [isLoading, setIsLoading] = useState(true);

  function login(data) {
    setUser(data.user);
    setAccessToken(data.access);
    setRefreshToken(data.refresh);

    sessionStorage.setItem("refreshToken", data.refresh);
  }

  async function logout() {
    const currentAccessToken = accessToken;
    const currentRefreshToken = refreshToken;

    try {
      if (currentAccessToken && currentRefreshToken) {
        await fetch(`${API_BASE_URL}/auth/logout/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${currentAccessToken}`,
          },
          body: JSON.stringify({
            refresh: currentRefreshToken,
          }),
        });
      }
    } finally {
      setUser(null);
      setAccessToken(null);
      setRefreshToken(null);

      sessionStorage.removeItem("refreshToken");
    }
  }

  useEffect(() => {
    async function restoreSession() {
      if (!refreshToken) {
        setIsLoading(false);
        return;
      }

      try {
        const refreshResponse = await fetch(
          `${API_BASE_URL}/auth/token/refresh/`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              refresh: refreshToken,
            }),
          }
        );

        if (!refreshResponse.ok) {
          logout();
          return;
        }

        const tokenData = await refreshResponse.json();

        setAccessToken(tokenData.access);

        if (tokenData.refresh) {
          setRefreshToken(tokenData.refresh);
          sessionStorage.setItem(
            "refreshToken",
            tokenData.refresh
          );
        }

        const userResponse = await fetch(
          `${API_BASE_URL}/auth/me/`,
          {
            headers: {
              Authorization: `Bearer ${tokenData.access}`,
            },
          }
        );

        if (!userResponse.ok) {
          logout();
          return;
        }

        const userData = await userResponse.json();

        setUser(userData);
      } catch {
        logout();
      } finally {
        setIsLoading(false);
      }
    }

    restoreSession();
  }, []);

  const value = {
    user,
    accessToken,
    refreshToken,
    isAuthenticated: Boolean(user && accessToken),
    isLoading,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}


export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used within an AuthProvider."
    );
  }

  return context;
}