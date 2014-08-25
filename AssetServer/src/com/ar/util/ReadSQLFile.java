package com.ar.util;

import java.io.InputStream;

import com.fss.util.Global;

public class ReadSQLFile
{
	private String mstrFileName = "";

	public ReadSQLFile(String strFileName)
	{
		mstrFileName = strFileName;
	}

	private String getLine(StringBuffer buf) throws Exception
	{
		try
		{
			int iIndex = buf.indexOf("\n");
			String strReturn;
			if (iIndex < 0)
			{
				strReturn = buf.toString();
				iIndex = buf.length() - 1;
				if (strReturn.equals(""))
				{
					strReturn = null;
				}
			}
			else
			{
				strReturn = buf.substring(0, iIndex);
			}
			buf.delete(0, iIndex + 1);
			return strReturn;
		}
		catch (Exception ex)
		{
			throw new Exception("Get line: " + ex.toString());
		}
	}

	private StringBuffer readTextFile() throws Exception
	{
		InputStream is = this.getClass().getResourceAsStream(mstrFileName);
		if (is == null)
		{
			throw new Exception("Can not read file " + mstrFileName + ".");
		}

		byte[] bt = new byte[8192];
		int iByteRead = 0;
		StringBuffer strBuf = new StringBuffer();
		while ((iByteRead = is.read(bt)) >= 0)
		{
			strBuf.append(new String(bt, 0, iByteRead, Global.ENCODE));
		}
		return strBuf;
	}

	public String getSQLQuery() throws Exception
	{
		String strSQLOut = "";
		try
		{
			StringBuffer strBufferContent = readTextFile();
			String strLine = "";
			while ((strLine = getLine(strBufferContent)) != null)
			{
				strSQLOut += " " + strLine.trim();
			}
			return strSQLOut;
		}
		catch (Exception ex)
		{
			ex.printStackTrace();
			throw ex;
		}
	}
}
