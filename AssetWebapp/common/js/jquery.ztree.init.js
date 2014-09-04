var setting = {
	data: {
		key: {
			title: "Press any keyword for filter data"
		},
		simpleData: {
			enable: true
		}
	},
	view: {
		fontCss: getFontCss,
		addHoverDom: addHoverDom,
		removeHoverDom: removeHoverDom,
		selectedMulti: false
	},
	edit: {
		enable: true,
		editNameSelectAll: true,
		showRemoveBtn: showRemoveBtn,
		showRenameBtn: showRenameBtn
	},
	callback: {
		beforeClick: beforeClick,
		onClick: onClick,
		beforeDrag: beforeDrag,
		beforeEditName: beforeEditName,
		beforeRemove: beforeRemove,
		beforeRename: beforeRename,
		onRemove: onRemove,
		onRename: onRename
	}
};

var zNodes =[
	{ name:"Máy móc, Thiết bị động lực", open:true,
		children: [
			{ name:"Máy phát động lực"},
			{ name:"Máy phát điện",open:true,
				children: [
					{ name:"Máy phát điện xăng"},
					{ name:"Máy phát điện dầu"},
					{ name:"Máy phát điện khác"}
				]},
			{ name:"Máy biến áp và thiết bị nguồn điện",name1:"Máy biến áp và thiết bị nguồn điện 1", isParent:true,open:true,
				children: [
					{ name:"Máy biến áp"},
					{ name:"ACU",isParent:true,open:true,
						children: [
							{ name:"ACU 2V"},
							{ name:"ACU 12V"},
							{ name:"ACU khác"}
						]
					},
					{ name:"Máy phát điện khác"}
				]
			}
		]},
	{ name:"Máy móc, Thiết bị công tác",open:true,
		children: [
			{ name:"pNode 21", open:true,
				children: [
					{ name:"leaf node 211"},
					{ name:"leaf node 212"},
					{ name:"leaf node 213"},
					{ name:"leaf node 214"}
				]},
			{ name:"pNode 22",open:true,
				children: [
					{ name:"leaf node 221"},
					{ name:"leaf node 222"},
					{ name:"leaf node 223"},
					{ name:"leaf node 224"}
				]},
			{ name:"pNode 23",open:true,
				children: [
					{ name:"leaf node 231"},
					{ name:"leaf node 232"},
					{ name:"leaf node 233"},
					{ name:"leaf node 234"}
				]}
		]},
	{ name:"pNode 3 - no child", isParent:true}

];
function beforeDrag(treeId, treeNodes) {
	return false;
}
function beforeEditName(treeId, treeNode) {
	className = (className === "dark" ? "":"dark");
	showLog("[ "+getTime()+" beforeEditName ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name);
	var zTree = $.fn.zTree.getZTreeObj("treeDemo");
	zTree.selectNode(treeNode);
	return confirm("Start node '" + treeNode.name + "' editorial status?");
}
function beforeRemove(treeId, treeNode) {
	className = (className === "dark" ? "":"dark");
	showLog("[ "+getTime()+" beforeRemove ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name);
	var zTree = $.fn.zTree.getZTreeObj("treeDemo");
	zTree.selectNode(treeNode);
	return confirm("Confirm delete node '" + treeNode.name + "' it?");
}
function onRemove(e, treeId, treeNode) {
	showLog("[ "+getTime()+" onRemove ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name);
}
function beforeRename(treeId, treeNode, newName, isCancel) {
	className = (className === "dark" ? "":"dark");
	showLog((isCancel ? "<span style='color:red'>":"") + "[ "+getTime()+" beforeRename ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name + (isCancel ? "</span>":""));
	if (newName.length == 0) {
		alert("Node name can not be empty.");
		var zTree = $.fn.zTree.getZTreeObj("treeDemo");
		setTimeout(function(){zTree.editName(treeNode)}, 10);
		return false;
	}
	return true;
}
function onRename(e, treeId, treeNode, isCancel) {
	showLog((isCancel ? "<span style='color:red'>":"") + "[ "+getTime()+" onRename ]&nbsp;&nbsp;&nbsp;&nbsp; " + treeNode.name + (isCancel ? "</span>":""));
}
function showRemoveBtn(treeId, treeNode) {
	return !treeNode.isFirstNode;
}
function showRenameBtn(treeId, treeNode) {
	return !treeNode.isLastNode;
}

var newCount = 1;
function addHoverDom(treeId, treeNode) {
	var sObj = $("#" + treeNode.tId + "_span");
	if (treeNode.editNameFlag || $("#addBtn_"+treeNode.tId).length>0) return;
	var addStr = "<span class='button add' id='addBtn_" + treeNode.tId
		+ "' title='add node' onfocus='this.blur();'></span>";
	sObj.after(addStr);
	var btn = $("#addBtn_"+treeNode.tId);
	if (btn) btn.bind("click", function(){
		var zTree = $.fn.zTree.getZTreeObj("treeDemo");
		zTree.addNodes(treeNode, {id:(100 + newCount), pId:treeNode.id, name:"new node" + (newCount++)});
		return false;
	});
};
function removeHoverDom(treeId, treeNode) {
	$("#addBtn_"+treeNode.tId).unbind().remove();
};

function focusKey(e) {
	if (key.hasClass("empty")) {
		key.removeClass("empty");
	}
}

function blurKey(e) {
	if (key.get(0).value === "") {
		key.addClass("empty");
	}
}
var lastValue = "", nodeList = [], fontCss = {};
function clickRadio(e) {
	lastValue = "";
	searchNode(e);
}
function searchNode(e) {
	var zTree = $.fn.zTree.getZTreeObj("treeDemo");
	var value = $.trim(key.get(0).value);
	var keyType = "";

	keyType = "name";
	if (key.hasClass("empty")) {
		value = "";
	}
	if (lastValue === value) return;
	lastValue = value;
	if (value === "") return;
	updateNodes(false);
	nodeList = zTree.getNodesByParamFuzzy(keyType, value);
	updateNodes(true);

}
function updateNodes(highlight) {
	var zTree = $.fn.zTree.getZTreeObj("treeDemo");
	for( var i=0, l=nodeList.length; i<l; i++) {
		nodeList[i].highlight = highlight;
		zTree.updateNode(nodeList[i]);
	}
}
function getFontCss(treeId, treeNode) {
	return (!!treeNode.highlight) ? {color:"#A60000", "font-weight":"bold"} : {color:"#333", "font-weight":"normal"};
}
function filter(node) {
	return !node.isParent && node.isFirstNode;
}

var key;
var log, className = "dark";
function beforeClick(treeId, treeNode, clickFlag) {
	className = (className === "dark" ? "":"dark");
	
	showLog("[ "+getTime()+" beforeClick ]&nbsp;&nbsp;" + treeNode.name );
	
	$("#asset_name").val(treeNode.name);
	return (treeNode.click != false);
}
function onClick(event, treeId, treeNode, clickFlag) {
	showLog("[ "+getTime()+" onClick ]&nbsp;&nbsp;clickFlag = " + clickFlag + " (" + (clickFlag===1 ? "single selected": (clickFlag===0 ? "<b>cancel selected</b>" : "<b>multi selected</b>")) + ")");
}		
function showLog(str) {
	if (!log) log = $("#log");
	
	log.append("<li class='"+className+"'>"+str+"</li>");
	
	if(log.children("li").length > 8) {
		log.get(0).removeChild(log.children("li")[0]);
	}
}
function getTime() {
	var now= new Date(),
	h=now.getHours(),
	m=now.getMinutes(),
	s=now.getSeconds();
	return (h+":"+m+":"+s);
}

function selectAll() {
	var zTree = $.fn.zTree.getZTreeObj("treeDemo");
	zTree.setting.edit.editNameSelectAll =  $("#selectAll").attr("checked");
}

$(document).ready(function(){
	$.fn.zTree.init($("#treeDemo"), setting, zNodes);
	$("#selectAll").bind("click", selectAll);
	key = $("#key");
	key.bind("focus", focusKey)
	.bind("blur", blurKey)
	.bind("propertychange", searchNode)
	.bind("input", searchNode);
	$("#name").bind("change", clickRadio);
	$("#level").bind("change", clickRadio);
	$("#id").bind("change", clickRadio);
	$("#getNodeByParam").bind("change", clickRadio);
	$("#getNodesByParam").bind("change", clickRadio);
	$("#getNodesByParamFuzzy").bind("change", clickRadio);
	$("#getNodesByFilter").bind("change", clickRadio);
	
});