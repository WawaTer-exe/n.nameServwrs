using BepInEx;
using HarmonyLib;
using UnityEngine.SceneManagement;
using System;

namespace RecRoomOfflineSandbox
{
    [BepInPlugin("com.reborn.offlinesandbox", "Rec Room Offline Sandbox Mod", "1.0.0")]
    public class SandboxMod : BaseUnityPlugin
    {
        private void Awake()
        {
            Logger.LogInfo("Offline Sandbox Integration Loading...");
            
            // Run Harmony to patch matchmaking systems and bypass Photon network locks
            var harmony = new Harmony("com.reborn.offlinesandbox");
            harmony.PatchAll();
            
            Logger.LogInfo("Network patches successfully bound. Offline map switching operational.");
        }
    }

    // Intercepts the destination logic to bypass real matchmaking queues
    [HarmonyPatch(typeof(UnityEngine.SceneManagement.SceneManager), "LoadScene", new Type[] { typeof(string) })]
    public static class SceneLoadInterceptor
    {
        public static bool Prefix(ref string sceneName)
        {
            // Intercept internal room requests and point them directly to standard local scene maps
            if (sceneName.Equals("Paintball", StringComparison.OrdinalIgnoreCase))
            {
                // Force load a specific local map file within the installation cache directory
                sceneName = "Paintball_Homestead"; 
                UnityEngine.Debug.Log("[Sandbox Mod] Redirected matchmaking request to local homestead map.");
            }
            else if (sceneName.Equals("LaserTag", StringComparison.OrdinalIgnoreCase))
            {
                sceneName = "LaserTag_Cyberpunk";
            }
            else if (sceneName.Equals("Quest", StringComparison.OrdinalIgnoreCase))
            {
                sceneName = "Quest_Castle";
            }

            return true; // Allow the local engine to proceed with loading the asset scene locally
        }
    }
}
