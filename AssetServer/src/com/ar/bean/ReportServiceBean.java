package com.ar.bean;

import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Date;

import ReportTDK.Report;

import com.ar.util.AppProcessor;
import com.ar.util.AppServer;
import com.ar.util.ReadSQLFile;
import com.ar.util.Util;
import com.fss.sql.Database;
import com.fss.util.StringUtil;

public class ReportServiceBean extends AppProcessor
{

	public void doGet() throws Exception
	{

	}

	@Override
	public void doPost() throws Exception
	{
		String request_type = request.getString("Method");
		switch (request_type)
		{
		case "DeviceReportByArea":
			String devLink = createDeviceReportByArea();
			response.put("FileOut", devLink);
			break;
		case "IssueReportByArea":
			String issueLink = createIssueReportByArea();
			response.put("FileOut", issueLink);
			break;
		case "form_report_issue_load":
			formReportIssueLoad();
			break;
		case "Test":
			response.put("FileOut", test());
			break;
		}

	}

	public void doDelete() throws Exception
	{

	}

	/**
	 * 
	 * @throws Exception
	 */
	public void formReportIssueLoad() throws Exception
	{
		ResultSet rs = null;
		PreparedStatement pstm = null;
		String strSQL = "";
		try
		{
			strSQL = "SELECT * FROM device ";
			// open connection
			open();
			// prepare
			pstm = mcnMain.prepareStatement(strSQL);
			// execute query
			rs = pstm.executeQuery();
			// put devices
			response.put("devices", Util.convertToJSONArray(rs));
			// close
			rs.close();
			pstm.close();
			//
			strSQL = "SELECT * FROM area WHERE level = 2 ";
			// prepare
			pstm = mcnMain.prepareStatement(strSQL);
			// execute query
			rs = pstm.executeQuery();
			// put devices
			response.put("areas", Util.convertToJSONArray(rs));
		}
		catch (Exception ex)
		{
			ex.printStackTrace();
			throw ex;
		}
		finally
		{
			Database.closeObject(rs);
			Database.closeObject(pstm);
			close();
		}
	}

	public String createDeviceReportByArea() throws Exception
	{
		ResultSet rs = null;
		PreparedStatement pstm = null;
		try
		{
			// template path
			String excelTemplatePath = AppServer.getParam("ExcelTemplatePath");
			String templatePath = AppServer.getParam("TemplatePath");
			String strReportOut = AppServer.getParam("ReportOut");
			String strFileName = "TemplateDeviceReportByArea";
			String strFileOut = strFileName
					+ StringUtil.format(new Date(), "yyyyMMddhhmmss");
			// String strFileOut = "dev_report";
			// read sql file
			String strSQL = new ReadSQLFile(templatePath + strFileName + ".sql")
					.getSQLQuery();
			// open connection
			open();
			// get parameter
			String strAreaCode = request.getString("area_code");
			String strStatus = request.getString("status");
			String strAreaSQL = "";
			// set sql parameter
			if (!strAreaCode.equals("ALL"))
			{
				strAreaSQL = " AND d.area_code ='" + strAreaCode + "' ";
			}
			strSQL = strSQL.replaceAll("<%p_area_code%>", strAreaSQL);

			if (!strStatus.equals("ALL"))
			{
				strAreaSQL = " AND d.status ='" + strStatus + "' ";
			}
			strSQL = strSQL.replaceAll("<%p_status%>", strAreaSQL);
			// prepare statement
			pstm = mcnMain.prepareStatement(strSQL);
			// execute query
			rs = pstm.executeQuery();
			// create report
			Report report = new Report(rs, excelTemplatePath + strFileName
					+ ".xls", strReportOut + strFileOut + ".xls");
			report.setParameter("$Report_Date",
					StringUtil.format(new Date(), "yyyy-MM-dd"));
			// fill data
			report.fillDataToExcel();
			// create file
			// createRealFile(strFileOut);
			// return link
			return strFileOut + ".xls";
		}
		catch (Exception ex)
		{
			ex.printStackTrace();
			throw ex;
		}
		finally
		{
			Database.closeObject(rs);
			Database.closeObject(pstm);
			close();
		}
	}

	public String test() throws Exception
	{
		ResultSet rs = null;
		PreparedStatement pstm = null;
		try
		{
			String excelTemplatePath = AppServer.getParam("ExcelTemplatePath");
			String templatePath = AppServer.getParam("TemplatePath");
			String strReportOut = AppServer.getParam("ReportOut");
			
			String strFileName = "Test";
			String strFileOut = strFileName
					+ StringUtil.format(new Date(), "yyyyMMddhhmmss");
			// read sql file
			String strSQL = new ReadSQLFile(templatePath + strFileName + ".sql")
					.getSQLQuery();
			// open connection
			open();
			// prepare statement
			pstm = mcnMain.prepareStatement(strSQL);
			// execute query
			rs = pstm.executeQuery();
			//Report
			Report report = new Report(rs, excelTemplatePath + strFileName
					+ ".xls", strReportOut + strFileOut + ".xls");
			report.setParameter("$Report_Date",
					StringUtil.format(new Date(), "yyyy-MM-dd"));
			// fill data
			report.fillDataToExcel();
			return strFileOut + ".xls";
		}
		catch (Exception ex)
		{
			ex.printStackTrace();
			throw ex;
		}
		finally
		{

		}
	}

	public String createIssueReportByArea() throws Exception
	{
		ResultSet rs = null;
		PreparedStatement pstm = null;
		try
		{
			// template path
			String excelTemplatePath = AppServer.getParam("ExcelTemplatePath");
			String templatePath = AppServer.getParam("TemplatePath");
			String strReportOut = AppServer.getParam("ReportOut");
			String strFileName = "TemplateIssueReportByArea";
			String strFileOut = strFileName
					+ StringUtil.format(new Date(), "yyyyMMddhhmmss");
			// String strFileOut = "issue_report";
			// read sql file
			String strSQL = new ReadSQLFile(templatePath + strFileName + ".sql")
					.getSQLQuery();
			// open connection
			open();
			
			// get parameter
			String strDeviceId = request.getString("device_id");
			String strDeviceSQL = "";
			String strAreaId = request.getString("area_id");
			String strAreaSQL = "";
			String strFromDate = request.getString("from_date");
			String strFromDateSQL = "";
			String strToDate = request.getString("to_date");
			String strToDateSQL = "";
			// set sql parameter
			if (!strDeviceId.equals("ALL"))
			{
				strDeviceSQL = " AND b.device_id ='" + strDeviceId + "' ";
			}
			if (!strAreaId.equals("ALL"))
			{
				strAreaSQL = " AND a.area_id ='" + strAreaId + "' ";
			}
			if (!strFromDate.equals(""))
			{
				strFromDateSQL = " AND b.issue_date >= STR_TO_DATE('"
						+ strFromDate + "','%d/%m/%Y') ";
			}
			if (!strToDate.equals(""))
			{
				strToDateSQL = " AND b.issue_date <= STR_TO_DATE('" + strToDate
						+ " 23:59:59','%d/%m/%Y %H:%i:%s') ";
			}
			strSQL = strSQL.replaceAll("<%p_device_id%>", strDeviceSQL);
			strSQL = strSQL.replaceAll("<%p_area_id%>", strAreaSQL);
			strSQL = strSQL.replaceAll("<%p_from_date%>", strFromDateSQL);
			strSQL = strSQL.replaceAll("<%p_to_date%>", strToDateSQL);
			// prepare statement
			pstm = mcnMain.prepareStatement(strSQL);
			// execute query
			rs = pstm.executeQuery();
			// create report
			Report report = new Report(rs, excelTemplatePath + strFileName
					+ ".xls", strReportOut + strFileOut + ".xls");
			report.setParameter("$Report_Date",
					StringUtil.format(new Date(), "yyyy-MM-dd"));
			// fill data
			report.fillDataToExcel();
			// create file
			// createRealFile(strFileOut);
			// return link
			return strFileOut + ".xls";
		}
		catch (Exception ex)
		{
			ex.printStackTrace();
			throw ex;
		}
		finally
		{
			Database.closeObject(rs);
			Database.closeObject(pstm);
			close();
		}
	}

}
