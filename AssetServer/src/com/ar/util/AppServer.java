package com.ar.util;

import java.sql.Connection;

import oracle.jdbc.pool.OracleConnectionPoolDataSource;

import com.fss.dictionary.Dictionary;
import com.fss.dictionary.DictionaryNode;
import com.microsoft.sqlserver.jdbc.SQLServerConnectionPoolDataSource;
import com.mysql.jdbc.jdbc2.optional.MysqlConnectionPoolDataSource;

public class AppServer
{
	private MysqlConnectionPoolDataSource poolMySQL = null;
	private static Dictionary mdic = null;
	private OracleConnectionPoolDataSource poolOracle = null;
	private SQLServerConnectionPoolDataSource  poolSQLServer = null;
	private static AppServer instanceOracle = null;
	private static AppServer instanceMySQL = null;
	private static AppServer instanceSQLServer = null;
	public static String getParam(String strKey)
	{
		return mdic.getString(strKey);
	}

	static
	{
		try
		{
			mdic = new Dictionary("conf/ServerConfig.txt");
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}

	/**
	 * <p>
	 * Copyright: Copyright (c) 2011
	 * </p>
	 * <p>
	 * Company: Smart Connect TM Co., Ltd
	 * </p>
	 * 
	 * @author TuanNA12
	 * @description
	 * @date
	 * @version 2.0
	 */
	private AppServer(String strTypeConn) throws Exception
	{
		if (strTypeConn.equals("Oracle"))
		{
			if (this.poolOracle == null)
			{
				poolOracle = createConnectionPool(strTypeConn);
			}
		}
		else if (strTypeConn.equals("MySQL"))
		{
			if (this.poolMySQL == null)
			{
				poolMySQL = createPoolMySQL(strTypeConn);
			}
		}
		else if (strTypeConn.equals("SQLServer"))
		{
			if (this.poolSQLServer == null)
			{
				poolSQLServer = createPoolSQLServer(strTypeConn);
			}
		}
		
	}
	/**
	 * <p>
	 * Copyright: Copyright (c) 2011
	 * </p>
	 * <p>
	 * Company: Smart Connect TM Co., Ltd
	 * </p>
	 * 
	 * @param strTypeConn
	 * @return
	 * @throws Exception
	 */
	private SQLServerConnectionPoolDataSource createPoolSQLServer(String strTypeConn)
			throws Exception
	{
		String strUrl = "";
		String strWillEncript = "";
		String strUserName = "";
		String strPassWord = "";
		String strKey = mdic.getString("EncryptKey");
		strWillEncript = mdic.getString("Encrypt");
		Encrypt enc = new Encrypt(strKey);
		String strNode = "";
		if (strTypeConn == null || strTypeConn.equals("SQLServer"))
		{
			strNode = "SQLServer";
			DictionaryNode ndConnection = mdic.getNode("Connection." + strNode);
			strUrl = ndConnection.getString("Url");

			strUserName = ndConnection.getString("UserName");
			strPassWord = ndConnection.getString("Password");
			if ((strWillEncript != null) && (strWillEncript.equals("Y")))
			{
				strPassWord = enc.decrypt(strPassWord);
			}
		}
		SQLServerConnectionPoolDataSource pool = new SQLServerConnectionPoolDataSource();
		pool.setURL(strUrl);
		pool.setDatabaseName("HANGHOA");
		pool.setUser(strUserName);
		pool.setPassword(strPassWord);
		return pool;
	}
	/**
	 * <p>
	 * Copyright: Copyright (c) 2011
	 * </p>
	 * <p>
	 * Company: Smart Connect TM Co., Ltd
	 * </p>
	 * 
	 * @param strTypeConn
	 * @return
	 * @throws Exception
	 */
	private MysqlConnectionPoolDataSource createPoolMySQL(String strTypeConn)
			throws Exception
	{
		String strUrl = "";
		String strWillEncript = "";
		String strUserName = "";
		String strPassWord = "";
		String strKey = mdic.getString("EncryptKey");
		strWillEncript = mdic.getString("Encrypt");
		Encrypt enc = new Encrypt(strKey);
		String strNode = "";
		if (strTypeConn == null || strTypeConn.equals("MySQL"))
		{
			strNode = "MySQL";
			DictionaryNode ndConnection = mdic.getNode("Connection." + strNode);
			strUrl = ndConnection.getString("Url");

			strUserName = ndConnection.getString("UserName");
			strPassWord = ndConnection.getString("Password");
			if ((strWillEncript != null) && (strWillEncript.equals("Y")))
			{
				strPassWord = enc.decrypt(strPassWord);
			}
		}
		MysqlConnectionPoolDataSource pool = new MysqlConnectionPoolDataSource();
		pool.setUrl(strUrl);
		pool.setUser(strUserName);
		pool.setPassword(strPassWord);
		return pool;
	}

	/**
	 * <p>
	 * Copyright: Copyright (c) 2011
	 * </p>
	 * <p>
	 * Company: Smart Connect TM Co., Ltd
	 * </p>
	 * 
	 * @author TuanNA12
	 * @description
	 * @date
	 * @version 2.0
	 */
	private OracleConnectionPoolDataSource createConnectionPool(
			String strTypeConn) throws Exception
	{
		String strUrl = "";
		String strWillEncript = "";
		String strUserName = "";
		String strPassWord = "";
		String strKey = mdic.getString("EncryptKey");
		strWillEncript = mdic.getString("Encrypt");
		Encrypt enc = new Encrypt(strKey);
		String strNode = "";
		if (strTypeConn == null || strTypeConn.equals("Oracle"))
		{
			strNode = "Oracle";
			DictionaryNode ndConnection = mdic.getNode("Connection." + strNode);
			strUrl = ndConnection.getString("Url");

			strUserName = ndConnection.getString("UserName");
			strPassWord = ndConnection.getString("Password");
			if ((strWillEncript != null) && (strWillEncript.equals("Y")))
			{
				strPassWord = enc.decrypt(strPassWord);
			}
		}
		return createConnectionPool(strUrl, strUserName, strPassWord);
	}

	/**
	 * <p>
	 * Copyright: Copyright (c) 2011
	 * </p>
	 * <p>
	 * Company: Smart Connect TM Co., Ltd
	 * </p>
	 * 
	 * @author TuanNA12
	 * @description
	 * @date
	 * @version 2.0
	 */
	private OracleConnectionPoolDataSource createConnectionPool(String strUrl,
			String strUserName, String strPassword) throws Exception
	{
		OracleConnectionPoolDataSource ods = new OracleConnectionPoolDataSource();
		ods.setURL(strUrl);
		ods.setUser(strUserName);
		ods.setPassword(strPassword);
		return ods;
	}

	/**
	 * <p>
	 * Copyright: Copyright (c) 2011
	 * </p>
	 * <p>
	 * Company: Smart Connect TM Co., Ltd
	 * </p>
	 * 
	 * @author TuanNA12
	 * @description
	 * @date
	 * @version 2.0
	 */
	public static AppServer getInstance(String strTypeConn) throws Exception
	{
		if (strTypeConn == null || strTypeConn.equals("Oracle"))
		{
			if (instanceOracle == null)
			{
				instanceOracle = new AppServer("Oracle");
			}
			return instanceOracle;

		}
		else if (strTypeConn == null || strTypeConn.equals("MySQL"))
		{
			if (instanceMySQL == null)
			{
				instanceMySQL = new AppServer("MySQL");
			}
			return instanceMySQL;

		}
		else if (strTypeConn == null || strTypeConn.equals("SQLServer"))
		{
			if (instanceSQLServer == null)
			{
				instanceSQLServer = new AppServer("SQLServer");
			}
			return instanceSQLServer;

		}
		throw new Exception("Unkown Instance");
	}
	/**
	 * <p>
	 * Copyright: Copyright (c) 2011
	 * </p>
	 * <p>
	 * Company: Smart Connect TM Co., Ltd
	 * </p>
	 * 
	 * @author TuanNA12
	 * @description
	 * @date
	 * @version 2.0
	 */
	public static Connection getConnection(String strTypeConn) throws Exception
	{
		if (strTypeConn.equals("Oracle"))
		{
			return getInstance(strTypeConn).poolOracle.getConnection();
		}
		else if (strTypeConn.equals("MySQL"))
		{
			return getInstance(strTypeConn).poolMySQL.getConnection();
		}
		/*else if (strTypeConn.equals("SQLServer"))
		{
			Class.forName("com.microsoft.sqlserver.jdbc.SQLServerDriver");
			String connectionUrl = "jdbc:sqlserver://10.15.30.101:1433;" +
			   "databaseName=HANGHOA;user=sa;password=123456;";
			Connection con = DriverManager.getConnection(connectionUrl);
//			Class.forName("sun.jdbc.odbc.JdbcOdbcDriver");
//			String connectionUrl = "jdbc:odbc:Driver={SQL Server};Server=10.15.30.101;Database=HangHoa;UserName=sa;Password=123456;";
//	        Connection con = DriverManager.getConnection(connectionUrl);	 
			return getInstance(strTypeConn).poolSQLServer.getConnection();
//	        return con;
		}*/
		return null;
	}

}
