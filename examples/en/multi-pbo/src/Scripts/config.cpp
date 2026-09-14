class CfgPatches
{
    class PBOExample_Scripts
    {
        units[] = {};
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] = { "PBOExample_Core", "DZ_Scripts" };
    };
};

class CfgMods
{
    class PBOExample
    {
        type = "mod";
        class defs
        {
            class gameScriptModule
            {
                value = "";
                files[] = { "PBOExample/Scripts/scripts/3_Game" };
            };
        };
    };
};
