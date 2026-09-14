class EntityPersistenceFixtureBattery extends Battery9V
{
    static const int SCHEMA_V1 = 1;
    static const int SCHEMA_V2 = 2;
    protected int m_Charges = 17;
    protected string m_Label = "matrix-v2-control";
    protected bool m_Locked;
    [NonSerialized()]
    protected bool m_OmitLockedOnSave = false;

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
        Print("[EntityPersistenceFixture] LOAD_FAIL variant=matrix stage=" + stage + " schema=" + schema + " engineVersion=" + engineVersion + " " + FixtureIdentity());
    }

    void SetFixtureLocked(bool locked)
    {
        m_Locked = locked;
        Print("[EntityPersistenceFixture] MATRIX_SET locked=" + m_Locked + " " + FixtureIdentity());
    }

    void SetFixtureCaseLabel(string caseLabel)
    {
        m_Label = caseLabel;
        Print("[EntityPersistenceFixture] MATRIX_SET case=" + m_Label + " " + FixtureIdentity());
    }

    void SetFixtureOmitLockedOnSave(bool omitLockedOnSave)
    {
        m_OmitLockedOnSave = omitLockedOnSave;
        Print("[EntityPersistenceFixture] MATRIX_SET omitLockedOnSave=" + m_OmitLockedOnSave + " " + FixtureIdentity());
    }

    int GetFixtureCharges()
    {
        return m_Charges;
    }

    string GetFixtureCaseLabel()
    {
        return m_Label;
    }

    bool GetFixtureLocked()
    {
        return m_Locked;
    }

    bool GetFixtureOmitLockedOnSave()
    {
        return m_OmitLockedOnSave;
    }

    override void OnStoreSave(ParamsWriteContext ctx)
    {
        super.OnStoreSave(ctx);

        bool wroteSchema = ctx.Write(SCHEMA_V2);
        bool wroteCharges = ctx.Write(m_Charges);
        bool wroteLabel = ctx.Write(m_Label);
        if (m_OmitLockedOnSave)
        {
            Print("[EntityPersistenceFixture] SAVE variant=matrix schema=2 locked=OMITTED wroteSchema=" + wroteSchema + " wroteCharges=" + wroteCharges + " wroteLabel=" + wroteLabel + " " + FixtureIdentity());
            return;
        }

        bool wroteLocked = ctx.Write(m_Locked);
        Print("[EntityPersistenceFixture] SAVE variant=matrix schema=2 locked=" + m_Locked + " wroteSchema=" + wroteSchema + " wroteCharges=" + wroteCharges + " wroteLabel=" + wroteLabel + " wroteLocked=" + wroteLocked + " " + FixtureIdentity());
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
        if (schema != SCHEMA_V1 && schema != SCHEMA_V2)
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

        if (schema == SCHEMA_V1)
        {
            m_Locked = false;
            Print("[EntityPersistenceFixture] LOAD_OK variant=matrix schema=1 migratedLocked=false charges=" + m_Charges + " engineVersion=" + engineVersion + " " + FixtureIdentity());
            return true;
        }

        if (!ctx.Read(m_Locked))
        {
            LogLoadFailure("locked-read", schema, engineVersion);
            return false;
        }

        Print("[EntityPersistenceFixture] LOAD_OK variant=matrix schema=2 locked=" + m_Locked + " charges=" + m_Charges + " engineVersion=" + engineVersion + " " + FixtureIdentity());
        return true;
    }
}
