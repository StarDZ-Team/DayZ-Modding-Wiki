class EntityPersistenceFixtureBattery extends Battery9V
{
    static const int SCHEMA_V1 = 1;
    protected int m_Charges = 17;
    protected string m_Label = "v1-control";

    protected string FixtureIdentity()
    {
        int persistentId1;
        int persistentId2;
        int persistentId3;
        int persistentId4;
        GetPersistentID(persistentId1, persistentId2, persistentId3, persistentId4);
        return "case=" + m_Label + " position=" + GetPosition() + " persistentId=" + persistentId1 + "/" + persistentId2 + "/" + persistentId3 + "/" + persistentId4;
    }

    protected void LogLoadFailure(string stage, int schema, int engineVersion)
    {
        Print("[EntityPersistenceFixture] LOAD_FAIL variant=v1 stage=" + stage + " schema=" + schema + " engineVersion=" + engineVersion + " " + FixtureIdentity());
    }

    void SetFixtureCaseLabel(string caseLabel)
    {
        m_Label = caseLabel;
        Print("[EntityPersistenceFixture] v1 set case=" + m_Label + " " + FixtureIdentity());
    }

    int GetFixtureCharges()
    {
        return m_Charges;
    }

    string GetFixtureCaseLabel()
    {
        return m_Label;
    }

    override void OnStoreSave(ParamsWriteContext ctx)
    {
        super.OnStoreSave(ctx);

        bool wroteSchema = ctx.Write(SCHEMA_V1);
        bool wroteCharges = ctx.Write(m_Charges);
        bool wroteLabel = ctx.Write(m_Label);
        Print("[EntityPersistenceFixture] v1 save schema=" + wroteSchema + " charges=" + wroteCharges + " label=" + wroteLabel);
    }

    override bool OnStoreLoad(ParamsReadContext ctx, int engineVersion)
    {
        if (!super.OnStoreLoad(ctx, engineVersion))
        {
            LogLoadFailure("parent", -1, engineVersion);
            return false;
        }

        int schema;
        if (!ctx.Read(schema))
        {
            LogLoadFailure("schema-read", -1, engineVersion);
            return false;
        }
        if (schema != SCHEMA_V1)
        {
            LogLoadFailure("unsupported-schema", schema, engineVersion);
            return false;
        }

        if (!ctx.Read(m_Charges))
        {
            LogLoadFailure("charges-read", schema, engineVersion);
            return false;
        }
        if (!ctx.Read(m_Label))
        {
            LogLoadFailure("label-read", schema, engineVersion);
            return false;
        }

        Print("[EntityPersistenceFixture] LOAD_OK variant=v1 schema=" + schema + " charges=" + m_Charges + " engineVersion=" + engineVersion + " " + FixtureIdentity());
        return true;
    }
}
