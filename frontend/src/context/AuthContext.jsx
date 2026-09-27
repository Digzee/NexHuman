import { API_BASE_URL } from "../config/api";
import {
  createContext,
  useContext,
  useEffect,
  useRef,
  useState,
} from "react";


const AuthContext = createContext(null);


export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [refreshToken, setRefreshToken] = useState(
    () => sessionStorage.getItem("refreshToken")
  );
  const [isLoading, setIsLoading] = useState(true);

  const accessTokenRef = useRef(null);
  const refreshTokenRef = useRef(
    sessionStorage.getItem("refreshToken")
  );

  function storeAccessToken(token) {
    accessTokenRef.current = token;
    setAccessToken(token);
  }

  function storeRefreshToken(token) {
    refreshTokenRef.current = token;
    setRefreshToken(token);

    if (token) {
      sessionStorage.setItem("refreshToken", token);
    } else {
      sessionStorage.removeItem("refreshToken");
    }
  }

  function clearSession() {
    setUser(null);
    storeAccessToken(null);
    storeRefreshToken(null);
  }

  function login(data) {
    setUser(data.user);
    storeAccessToken(data.access);
    storeRefreshToken(data.refresh);
  }

  async function refreshAccessToken() {
    const currentRefreshToken =
      refreshTokenRef.current;

    if (!currentRefreshToken) {
      clearSession();
      return null;
    }

    try {
      const response = await fetch(
        `${API_BASE_URL}/auth/token/refresh/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            refresh: currentRefreshToken,
          }),
        }
      );

      if (!response.ok) {
        clearSession();
        return null;
      }

      const data = await response.json();

      storeAccessToken(data.access);

      if (data.refresh) {
        storeRefreshToken(data.refresh);
      }

      return data.access;
    } catch {
      clearSession();
      return null;
    }
  }

  async function authenticatedFetch(
    url,
    options = {}
  ) {
    let token = accessTokenRef.current;

    if (!token) {
      token = await refreshAccessToken();
    }

    if (!token) {
      throw new Error(
        "Authentication is required."
      );
    }

    function createRequestOptions(
      requestToken
    ) {
      return {
        ...options,
        headers: {
          ...options.headers,
          Authorization: `Bearer ${requestToken}`,
        },
      };
    }

    let response = await fetch(
      url,
      createRequestOptions(token)
    );

    if (response.status !== 401) {
      return response;
    }

    const refreshedToken =
      await refreshAccessToken();

    if (!refreshedToken) {
      return response;
    }

    response = await fetch(
      url,
      createRequestOptions(refreshedToken)
    );

    return response;
  }

  async function logout() {
    const currentAccessToken =
      accessTokenRef.current;

    const currentRefreshToken =
      refreshTokenRef.current;

    try {
      if (currentAccessToken && currentRefreshToken) {
        await fetch(
          `${API_BASE_URL}/auth/logout/`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization:
                `Bearer ${currentAccessToken}`,
            },
            body: JSON.stringify({
              refresh: currentRefreshToken,
            }),
          }
        );
      }
    } finally {
      clearSession();
    }
  }

  useEffect(() => {
    async function restoreSession() {
      const storedRefreshToken =
        refreshTokenRef.current;

      if (!storedRefreshToken) {
        setIsLoading(false);
        return;
      }

      try {
        const restoredAccessToken =
          await refreshAccessToken();

        if (!restoredAccessToken) {
          return;
        }

        const userResponse = await fetch(
          `${API_BASE_URL}/auth/me/`,
          {
            headers: {
              Authorization:
                `Bearer ${restoredAccessToken}`,
            },
          }
        );

        if (!userResponse.ok) {
          clearSession();
          return;
        }

        const userData =
          await userResponse.json();

        setUser(userData);
      } catch {
        clearSession();
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
    isAuthenticated: Boolean(
      user && accessToken
    ),
    isLoading,
    login,
    logout,
    authenticatedFetch,
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