"use client";

import { useEffect } from "react";
import { supabase } from "../../lib/supabase";

export default function Dashboard() {

  useEffect(() => {

    // 🔥 THIS IS THE FIX
    const { data: listener } = supabase.auth.onAuthStateChange(
      async (event, session) => {

        console.log("EVENT:", event);
        console.log("SESSION:", session);

        if (session) {
          const token = session.access_token;

          // 🚀 redirect to Streamlit
          window.location.href = `https://ai-oracle-assistant.streamlit.app?token=${token}`;
        }
      }
    );

    return () => {
      listener.subscription.unsubscribe();
    };

  }, []);

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h2>Logging you in... 🚀</h2>
    </div>
  );
}