package com.ar.Model;

public class DeviceModelLog
{
	public int ID;
	public String Code;
	public int Area_id;
	public String Area_Code;
	public String Status;
	public String Address;
	public double Lat;
	public double Long;
	public int Reason_id;
	public int Device_infor_id;
	public double Old_value;
	public double New_value;

	public int getID()
	{
		return ID;
	}

	public void setID(int iD)
	{
		ID = iD;
	}

	public String getCode()
	{
		return Code;
	}

	public void setCode(String code)
	{
		Code = code;
	}

	public int getArea_id()
	{
		return Area_id;
	}

	public void setArea_id(int area_id)
	{
		Area_id = area_id;
	}

	public String getArea_Code()
	{
		return Area_Code;
	}

	public void setArea_Code(String area_Code)
	{
		Area_Code = area_Code;
	}

	public String getStatus()
	{
		return Status;
	}

	public void setStatus(String status)
	{
		Status = status;
	}

	public String getAddress()
	{
		return Address;
	}

	public void setAddress(String address)
	{
		Address = address;
	}

	public double getLat()
	{
		return Lat;
	}

	public void setLat(double lat)
	{
		Lat = lat;
	}

	public double getLong()
	{
		return Long;
	}

	public void setLong(double l)
	{
		Long = l;
	}

	public int getReason_id()
	{
		return Reason_id;
	}

	public void setReason_id(int reason_id)
	{
		Reason_id = reason_id;
	}

	public int getDevice_infor_id()
	{
		return Device_infor_id;
	}

	public void setDevice_infor_id(int device_infor_id)
	{
		Device_infor_id = device_infor_id;
	}

	public double getOld_value()
	{
		return Old_value;
	}

	public void setOld_value(double old_value)
	{
		Old_value = old_value;
	}

	public double getNew_value()
	{
		return New_value;
	}

	public void setNew_value(double new_value)
	{
		New_value = new_value;
	}

}
