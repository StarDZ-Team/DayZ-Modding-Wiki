class CfgPatches
{
    class PBOExample_Server
    {
        units[] = {};
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] = { "PBOExample_Scripts" };
    };
};

class CfgMods
{
    class PBOExampleServer
    {
        type = "mod";
        dependencies[] = { "Mission" };
        class defs
        {
            class missionScriptModule
            {
                value = "";
                files[] = { "PBOExample/Server/scripts/5_Mission" };
            };
        };
    };
};
