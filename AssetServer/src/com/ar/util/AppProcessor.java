package com.ar.util;


import java.sql.Connection;

import com.fss.sql.Database;
/**
 * <p>Title: </p>
 * <p>Description: </p>
 * <p>Copyright: Copyright (c) 2013</p>
 * @author Ngo Anh Tuan
 * @version 1.0
 */

public abstract class AppProcessor extends DatabaseProcessor
{
	
	/////////////////////////////////////////////////////////////////
	/**
	 * Create new processor
	 */
	/////////////////////////////////////////////////////////////////
	public AppProcessor()
	{
	}
	/**
	 * <p>Copyright: Copyright (c) 2013</p>
	 * @author Ngo ANh Tuan
	 * @version 1.0
	 * @date 04/10/2013
	 */
	public void open() throws Exception
	{
		try
		{
			mcnMain = (Connection) AppServer.getConnection("Oracle");
		}
		catch(Exception ex)
		{
			throw ex;
		}
	}
	/**
	 * <p>Copyright: Copyright (c) 2013</p>
	 * @author TuanNA12
	 * @version 1.0
	 * @date 04/10/2013
	 */
	public void close ()
	{
		if (mcnMain != null)
		{
			Database.closeObject(mcnMain);
			mcnMain = null;
		}
	}
	
	public abstract void doGet() throws Exception;
	
	public abstract void doPost() throws Exception;
	
	public abstract void doDelete() throws Exception;
}

