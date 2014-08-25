package com.ar.util;

public class DataHolder {
	private static String reportPath;

	public static String getReportPath() {
		return reportPath;
	}

	public static void setReportPath(String reportPath) {
		DataHolder.reportPath = reportPath;
	}

}
