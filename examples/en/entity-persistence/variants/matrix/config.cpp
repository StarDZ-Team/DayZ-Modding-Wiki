class CfgPatches
{
    class EntityPersistenceFixture
    {
        units[] = { "EntityPersistenceFixtureBattery" };
        weapons[] = {};
        requiredVersion = 0.1;
        requiredAddons[] = { "DZ_Gear_Consumables" };
    };
};

class CfgVehicles
{
    class Battery9V;
    class EntityPersistenceFixtureBattery : Battery9V
    {
        scope = 2;
        displayName = "Entity persistence fixture battery";
        descriptionShort = "Per-instance v2 persistence matrix fixture; inherits Battery9V art and item configuration.";
    };
};

class CfgMods
{
    class EntityPersistenceFixture
    {
        type = "mod";
        dependencies[] = { "World" };
        class defs
        {
            class worldScriptModule
            {
                value = "";
                files[] = { "EntityPersistenceFixture/scripts/4_World" };
            };
        };
    };
};
