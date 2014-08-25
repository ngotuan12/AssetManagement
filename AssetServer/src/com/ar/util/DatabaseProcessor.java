package com.ar.util;

import java.sql.Connection;

import org.codehaus.jettison.json.JSONObject;

/**
 * <p>Title: </p>
 * <p>Description: </p>
 * <p>Copyright: Copyright (c) 2013</p>
 * <p>Company: </p>
 * @author Ngo Anh Tuan
 * @version 1.0
 */

public abstract class DatabaseProcessor
{
	protected JSONObject request = null;
	protected JSONObject response = null;
	/////////////////////////////////////////////////////////////////
	// Variables
	/////////////////////////////////////////////////////////////////
	protected Connection mcnMain = null; // Used to update database
	/**
	 * Open connection to database
	 * @throws Exception
	 */
	public abstract void open() throws Exception;
	/**
	 * Open connection to database
	 * @param bAutoCommit if true then new transaction created
	 * @throws java.lang.Exception
	 * @author Ngo Anh Tuan
	 */
	public void open(boolean bAutoCommit) throws Exception
	{
		open();
		mcnMain.setAutoCommit(bAutoCommit);
	}
	/**
	 * Release database connection
	 * @author Ngo Anh Tuan
	 */
	public abstract void close();
	/**
	 *
	 * @throws Throwable
	 */
	public void finalize() throws Throwable
	{
		close();
		super.finalize();
	}
	public JSONObject getRequest()
	{
		return request;
	}
	public JSONObject getResponse()
	{
		return response;
	}
	public void setRequest(JSONObject request)
	{
		this.request = request;
	}
	
	public void setResponse(JSONObject response)
	{
		this.response = response;
	}
}
