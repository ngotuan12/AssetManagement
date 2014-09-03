package com.ar.util;

import java.io.PrintWriter;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.Date;
import java.util.HashMap;
import java.util.Scanner;

import javax.crypto.SecretKey;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.codehaus.jettison.json.JSONArray;
import org.codehaus.jettison.json.JSONException;
import org.codehaus.jettison.json.JSONObject;

import com.fss.dictionary.Dictionary;
import com.fss.dictionary.DictionaryNode;
import com.fss.util.AppException;
import com.fss.util.DateUtil;
import com.fss.util.StringUtil;

public class Util
{
	public static Dictionary mDic;
	public static HashMap<String, SecretKey> session = new HashMap<>();
	static
	{
		try
		{
			mDic = new Dictionary("conf/RequestConfig.txt");
		}
		catch (Exception ex)
		{
			ex.printStackTrace();
		}
	}

	public static JSONArray concatArray(JSONArray... arrs) throws JSONException
	{
		JSONArray result = new JSONArray();
		for (JSONArray arr : arrs)
		{
			for (int i = 0; i < arr.length(); i++)
			{
				result.put(arr.get(i));
			}
		}
		return result;
	}

	/**
	 * @param request
	 *            JSONObject contain request data
	 * @param response
	 * @throws Exception
	 */
	public static void processRequest(HttpServletRequest servletRequest,
			HttpServletResponse servletResponse) throws Exception
	{
		// response
		servletResponse.setCharacterEncoding("utf-8");
		servletResponse.setContentType("text/plain");
		servletResponse.setHeader("Access-Control-Allow-Origin", "* ");
		servletResponse
				.setHeader("Access-Control-Allow-Headers",
						"Origin, X-Requested-With, Content-Type, Accept, Authorization");
		servletResponse.setHeader("Access-Control-Allow-Methods",
				"POST, GET, OPTIONS");
		JSONObject jsonResponse = new JSONObject();
		JSONObject jsonRequest;
		Scanner scanner = null;
		try
		{
			String autKey = servletRequest.getHeader("Authorization");
			if (autKey == null)
			{
				return;
			}
			// get parameter
			String strServiceName = servletRequest.getServletPath();
			String strMethodName = servletRequest.getMethod();
			// get service config
			DictionaryNode ndClassConfig = mDic.getNode(strServiceName);
			if (ndClassConfig == null)
			{
				throw new Exception("unknown request " + strServiceName);
			}
			// request
			StringBuilder stringBuilder = new StringBuilder(1000);
			scanner = new Scanner(servletRequest.getInputStream(),"utf-8");
			while (scanner.hasNextLine())
			{
				stringBuilder.append(scanner.nextLine());
			}
			String strRequest = stringBuilder.toString();
			System.out.println(strRequest);
			// JSON request
			// jsonRequest = new JSONObject("{}");
			jsonRequest = new JSONObject(strRequest);
			// check session
			if (!strServiceName.equals("/PermissionService")&&!strServiceName.equals("/AuthorizationService"))
			{
				// String strMethod =
				// StringUtil.nvl(jsonRequest.getString("Method"), "");
				checkSessionUser(jsonRequest.getString("SessionUserName"),
						autKey);
			}
			else if (!StringUtil.nvl(jsonRequest.getString("Method"), "")
					.equals("login")) checkSessionUser(
					jsonRequest.getString("SessionUserName"), autKey);
			// Get class name & create class instance
			String strClassName = ndClassConfig.getString("Class");
			if (strClassName.length() == 0) throw new Exception(
					"Class name was not passed");
			@SuppressWarnings("rawtypes")
			Class cls = Class.forName(strClassName);
			Object obj = cls.newInstance();

			// Check class
			if (!(obj instanceof DatabaseProcessor)) throw new Exception(
					"Class '" + strClassName + "' must be a Database Processor");
			DatabaseProcessor storage = (DatabaseProcessor) obj;
			// Get function name and method
			String strFunctionName = "";
			switch (strMethodName.toUpperCase())
			{
			case "GET":
				strFunctionName = "doGet";
				break;
			case "POST":
				strFunctionName = "doPost";
				break;
			case "DELETE":
				strFunctionName = "doDelete";
				break;
			default:
				throw new Exception("method is unsupport");
			}
			if (strFunctionName.length() == 0) throw new Exception(
					"Function name was not passed");
			// Get method from class name and function name
			@SuppressWarnings("unchecked")
			Method method = cls.getMethod(strFunctionName);
			if (method == null) throw new Exception("Function '" + strClassName
					+ "." + strFunctionName + "' was not declared");

			// Check function
			if (Modifier.isAbstract(method.getModifiers())) throw new Exception(
					"Function '" + strClassName + "." + strFunctionName
							+ "' was not implemented");
			if (!Modifier.isPublic(method.getModifiers())) throw new Exception(
					"Function '" + strClassName + "." + strFunctionName
							+ "' is not public");
			// Invoke function
			storage.setRequest(jsonRequest);
			storage.setResponse(jsonResponse);
			try
			{
				obj = method.invoke(storage);
				// response.put("handle", strHandle);
			}
			catch (InvocationTargetException e)
			{
				if (e.getTargetException() instanceof Exception) throw (Exception) e
						.getTargetException();
				throw new Exception(e.getTargetException());
			}
			jsonResponse.put("handle", "on_success");
		}
		catch (AppException aex)
		{
			aex.printStackTrace();
			jsonResponse.put("handle", "on_error");
			jsonResponse.put("code", aex.getReason());
			jsonResponse.put("message", aex.getMessage());
		}
		catch (JSONException jex)
		{
			jex.printStackTrace();
			jsonResponse.put("handle", "on_error");
			jsonResponse.put("code", "JSON-ERROR");
			jsonResponse.put("message", jex.getMessage());
		}
		catch (Exception ex)
		{
			ex.printStackTrace();
			jsonResponse.put("handle", "on_error");
			jsonResponse.put("code", "SYS-ERROR");
			jsonResponse.put("message", ex.getMessage());
		}
		finally
		{
			if(scanner!=null)
				scanner.close();
			// return response
			PrintWriter out = servletResponse.getWriter();
			out.println(jsonResponse.toString());
			out.flush();
		}
	}

	public static void checkSessionUser(String strUserName, String strSessionKey)
			throws Exception
	{
		try
		{
			SecretKey desKey = session.get(strSessionKey);
			Encrypt desEncrypter = new Encrypt(desKey, desKey.getAlgorithm());
			String strInfor = desEncrypter.decrypt(strSessionKey);
			JSONObject jsonInfor = new JSONObject(strInfor);
			// check session username
			if (!jsonInfor.getString("username").equals(strUserName))
			{
				throw new AppException("EAS-SYS-001",
						"Session user name not correct!");
			}
			Date dateExpire = DateUtil.toDate(jsonInfor.getString("date"),
					"dd/MM/yyyy HH:mm:ss");
			// check session expire
			if (dateExpire.compareTo(new Date()) < 0)
			{
				throw new AppException("EAS-SYS-002", "Session expire!");
			}
		}
		catch (AppException aex)
		{
			throw aex;
		}
		catch (Exception ex)
		{
			ex.printStackTrace();
			throw new AppException("EAS-SYS-004","Authenticate false!");
		}
	}

	/**
	 * @param rs
	 * @return
	 * @throws SQLException
	 * @throws JSONException
	 */
	public static JSONArray convertToJSONArray(ResultSet rs)
			throws SQLException, JSONException
	{
		JSONArray json = new JSONArray();
		ResultSetMetaData rsmd = rs.getMetaData();

		while (rs.next())
		{
			int numColumns = rsmd.getColumnCount();
			JSONObject obj = new JSONObject();
			for (int i = 1; i < numColumns + 1; i++)
			{
				String column_name = rsmd.getColumnLabel(i);

				if (rsmd.getColumnType(i) == java.sql.Types.ARRAY)
				{
					obj.put(column_name, rs.getArray(column_name));
				}
				else if (rsmd.getColumnType(i) == java.sql.Types.BIGINT)
				{
					obj.put(column_name, rs.getInt(column_name));
				}
				else if (rsmd.getColumnType(i) == java.sql.Types.BOOLEAN)
				{
					obj.put(column_name, rs.getBoolean(column_name));
				}
				else if (rsmd.getColumnType(i) == java.sql.Types.BLOB)
				{
					obj.put(column_name, rs.getBlob(column_name));
				}
				else if (rsmd.getColumnType(i) == java.sql.Types.DOUBLE)
				{
					obj.put(column_name, rs.getDouble(column_name));
				}
				else if (rsmd.getColumnType(i) == java.sql.Types.FLOAT)
				{
					obj.put(column_name, rs.getFloat(column_name));
				}
				else if (rsmd.getColumnType(i) == java.sql.Types.INTEGER)
				{
					obj.put(column_name, rs.getInt(column_name));
				}
				else if (rsmd.getColumnType(i) == java.sql.Types.NVARCHAR)
				{
					obj.put(column_name, rs.getNString(column_name));
				}
				else if (rsmd.getColumnType(i) == java.sql.Types.VARCHAR)
				{
					obj.put(column_name, rs.getString(column_name));
				}
				else if (rsmd.getColumnType(i) == java.sql.Types.TINYINT)
				{
					obj.put(column_name, rs.getInt(column_name));
				}
				else if (rsmd.getColumnType(i) == java.sql.Types.SMALLINT)
				{
					obj.put(column_name, rs.getInt(column_name));
				}
				else if (rsmd.getColumnType(i) == java.sql.Types.DATE)
				{
					obj.put(column_name, rs.getDate(column_name));
				}
				else if (rsmd.getColumnType(i) == java.sql.Types.TIMESTAMP)
				{
					obj.put(column_name, rs.getTimestamp(column_name));
				}
				else
				{
					obj.put(column_name, rs.getObject(column_name));
				}
			}
			json.put(obj);
		}

		return json;
	}
}
