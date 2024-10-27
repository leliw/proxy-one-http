import pytest

from app.features.sessions.parsers.html_parser import HtmlPage


@pytest.fixture
def body() -> str:
    return """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" >
<head><title>
	alfaRecordingsViewer
</title><meta http-equiv="Content-Type" content="text/html; charset=utf-8" /><meta name="Description" content="Przeglądarka nagrań systemu alfaPDS." /><meta name="Copyright" content="Alfavox Sp. z o.o." /><meta http-equiv="pragma" content="no-cache" /><meta http-equiv="X-UA-Compatible" content="IE=9" /><meta http-equiv="cache-control" content="no-store,no-cache,must-revalidate" /><meta http-equiv="cache-control" content="post-check=0,pre-check=0" /><link rel="icon" href="App_Themes/Alfavox/telephone_play.png" />
<link href="jPlayer/2.9.2/skin/blue.monday/css/jplayer.blue.monday.css" rel="stylesheet" type="text/css" /><link href="jPlayer/jplayerExtension/jplayer.extension.css" rel="stylesheet" />
    <style type="text/css">
        /* Override RadGrid Fonts  */
        .RadGrid, 
        .RadGrid .rgMasterTable,
        .RadGrid .rgDetailTable,
        .RadGrid .rgGroupPanel table,
        .RadGrid .rgCommandRow table,
        .RadGrid .rgEditForm table,
        .RadGrid .rgPager table,
        .RadGrid .rgGroupHeader,
        .GridToolTip
        {  
            font-family: Tahoma !important;
            font-size: 11px !important;
        }

        .RadGrid .rgRow TD,
        .RadGrid .rgAltRow TD,
        .RadGrid .rgHeader
        {
            padding: 2px !important;
            border-right-style: solid !important;
            border-right-width: 1px !important;
            border-right-color: #e2e2e2 !important;
        }
        
        /* Override RadListBox Font style  */
        .RadListBox span.rlbText  
        {  
           font-family: Tahoma;
           font-size: 11px;
        }
        .RadComboBox .rcbInputCell .rcbInput
        {
           font-family: Tahoma;
           font-size: 11px;
        }
        
        .RadComboBoxDropDown,
        .RadComboBoxDropDown .rcbItem,
        .RadComboBoxDropDown .rcbHovered
        {
           font-family: Tahoma;
           font-size: 11px;
        }
        
        /* RadDatePicker */
        div.RadPicker .rcTable .riTextBox, 
        table.RadCalendar .rcMainTable 
        {
           font-family: Tahoma;
           font-size: 11px;
        }
        
        table.RadCalendarTimeView
        {
           font-family: Tahoma !important;
           font-size: 11px !important;
        }
        
        .RadTreeList .rtlTable
        {
           font-family: Tahoma !important;
           font-size: 11px !important;
        }
        
        .RadInput .riTextBox, .RadComboBox .rcbInputCell .rcbInput
        {
           font-family: Tahoma !important;
           font-size: 11px !important;
        }
     </style>
     
     
     <script type="text/javascript">

         setInterval(function(){
             var iframes = document.getElementsByClassName("rwTable");
             for(var i = 0; i < iframes.length; i++){
                 try{
                     iframes[i].parentElement.getElementsByTagName("iframe")[0].style.height = (iframes[i].style.height-10);
                 }catch(e){
		
                 }
             }}, 1000);


         function logJSErrors(errObj) {
             var img = new Image;
             var docState = "unknown";
             try {
                 docState = document.readyState;
             }
             catch (e) {
                 docState = "Error retrieving document readyState: " + e.message;
             }

             img.src = "Default.aspx?cmd=log&err_msg=" + encodeURIComponent(errObj.message) +
                            "&documentState=" + encodeURIComponent(docState) +
                            "&line=" + encodeURIComponent(errObj.lineNumber) +
                            "&url=" + encodeURIComponent(errObj.fileName) +
                            "&browser=" + encodeURIComponent(errObj.browserInfo);
         }

         try {
             window.onerror = function(msg, url, line) {
                 try {
                     logJSErrors({ message: msg,
                         lineNumber: line,
                         fileName: url,
                         browserInfo: window.navigator.userAgent
                     });

                     if ('False' == 'True' || 'False' == 'True') {
                         if (typeof $ !== "undefined" && typeof $.myGrowlUI !== "undefined")
                             $.myGrowlUI('JavaScript Error', msg);
                         else
                             alert("[JavaScript ERROR] " + msg);
                     }
                 } catch (e) {
                     alert('[onerror] Error: ' + e.message);
                 }
                 return false; //return (isDebug === 1) ? false : true;
             }
         } catch (e) {
            logJSErrors(e);
            alert('[errorHandlerAttach] Error: ' + e.message);
         }

         function PerformAjaxRequestToKeepViewState()
         {
             // COM-253
             var ajaxPanel = $find('ctl00_apHelperAjaxPanel');
             if (ajaxPanel && typeof ajaxPanel.ajaxRequest === 'function')
                 ajaxPanel.ajaxRequest('AjaxCallUsedToKeepViewState');
         }
     </script>
     <link href="App_Themes/Alfavox/styles.css?v=19.7.0.309" type="text/css" rel="stylesheet" /><link href="/alfaRecordingsViewer/Telerik.Web.UI.WebResource.axd?d=F16azSOBtkPpv7x81kdj5j3UZhnZbh8sppKisZaSpRaJZHGm4jNKID43B5OGynXySrhanvHBKlrCL60wNpnNiISTvG0Ba1dKmGcmz3hiLJSwlKLdIrlkqMxCjrgZPPmSHEHa3hJLME_dCSA1lDSVag2&amp;t=638568676377359528&amp;compress=1&amp;_TSM_CombinedScripts_=%3b%3bTelerik.Web.UI%2c+Version%3d2020.1.219.40%2c+Culture%3dneutral%2c+PublicKeyToken%3d121fae78165ba3d4%3apl-PL%3ad010718b-d2d4-4e34-a63a-374109c08bc7%3a45085116%3a27c5704c%3aaac1aeb7%3ac73cf106" type="text/css" rel="stylesheet" /></head>
<body>
    <form name="aspnetForm" method="post" action="./Login.aspx" onsubmit="javascript:return WebForm_OnSubmit();" onkeypress="javascript:return WebForm_FireDefaultButton(event, 'ctl00_cphMain_btnLoginHash')" id="aspnetForm">
<div>
<input type="hidden" name="__LASTFOCUS" id="__LASTFOCUS" value="" />
<input type="hidden" name="ctl00_scriptManager_TSM" id="ctl00_scriptManager_TSM" value="" />
<input type="hidden" name="ctl00_RadStyleSheetManager1_TSSM" id="ctl00_RadStyleSheetManager1_TSSM" value="" />
<input type="hidden" name="__EVENTTARGET" id="__EVENTTARGET" value="" />
<input type="hidden" name="__EVENTARGUMENT" id="__EVENTARGUMENT" value="" />
<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="/wEPaA8FDzhkY2UyZTkwNzMwMzM2YxgBBR5fX0NvbnRyb2xzUmVxdWlyZVBvc3RCYWNrS2V5X18WAgUZY3RsMDAkbHNMb2dpblN0YXR1cyRjdGwwMQUZY3RsMDAkbHNMb2dpblN0YXR1cyRjdGwwM8unQdeRjsThPfR5FibaSamdGS7I7zKpU90CEwPCAVWY" />
</div>

<script type="text/javascript">
//<![CDATA[
var theForm = document.forms['aspnetForm'];
function __doPostBack(eventTarget, eventArgument) {
    if (!theForm.onsubmit || (theForm.onsubmit() != false)) {
        theForm.__EVENTTARGET.value = eventTarget;
        theForm.__EVENTARGUMENT.value = eventArgument;
        theForm.submit();
    }
}
//]]>
</script>


<script src="/alfaRecordingsViewer/WebResource.axd?d=9jasLgn5Au2mKJGg_mmslS71E_zvDfl0aLK7UR2ofPbCGEJRgPxYIgsRlKac9WtQXHmj3XzLp5iAI82LKE9NpgA3MnX-kpDL4PTfomPmJN41&amp;t=638568676371266408" type="text/javascript"></script>


<script src="/alfaRecordingsViewer/ScriptResource.axd?d=ehFLZVJ_j7HN0czxWmBQVkOQBZxwa_8s74mlXofJo2Rr9xC4Z7n95DSq1JlhKW-H7NrHET8KNi60rfsdGjEH4UXZ0v-voLOxpynrFTgpjBQwyHb1IsfuosfJPenss0x_-JerxFSwbKz2r8sUHL4dkEw-E2oBSyP0-W6wu42NknQ1&amp;t=ffffffffba22f784" type="text/javascript"></script>
<script src="/alfaRecordingsViewer/Telerik.Web.UI.WebResource.axd?_TSM_HiddenField_=ctl00_scriptManager_TSM&amp;compress=1&amp;_TSM_CombinedScripts_=%3b%3bSystem.Web.Extensions%2c+Version%3d4.0.0.0%2c+Culture%3dneutral%2c+PublicKeyToken%3d31bf3856ad364e35%3apl-PL%3aceece802-cb39-4409-a6c9-bfa3b2c8bf10%3aea597d4b%3ab25378d2%3bTelerik.Web.UI%3apl-PL%3ad010718b-d2d4-4e34-a63a-374109c08bc7%3a16e4e7cd%3af7645509%3a22a6274a%3aed16cbdc%3a88144a7a%3a33715776%3ab7778d6c" type="text/javascript"></script>
<script src="jquery.blockUI.js?ver=2" type="text/javascript"></script>
<script src="jPlayer/2.9.2/jplayer/jquery.jplayer.min.js" type="text/javascript"></script>
<script src="jPlayer/2.9.2/add-on/jplayer.playlist.min.js" type="text/javascript"></script>
<script src="jPlayer/2.9.2/add-on/jquery.jplayer.inspector.js" type="text/javascript"></script>
<script src="log4javascript/log4javascript.js" type="text/javascript"></script>
<script src="js/jquery-cookie-1.4.1/jquery.cookie-1.4.1.min.js" type="text/javascript"></script>
<script src="jPlayer/jPlayer.playerStart.js" type="text/javascript"></script>
<script src="js/popcorn/popcorn.min.js" type="text/javascript"></script>
<script src="js/syncAudioAndVideo/syncAudioVideo.js" type="text/javascript"></script>
<script src="js/resizeSensor/ResizeSensor.js" type="text/javascript"></script>
<script src="js/bundles/bundle.js" type="text/javascript"></script>
<script src="/alfaRecordingsViewer/WebResource.axd?d=0ampt5LM23Y2S9Js0y4E5uuy1w-HkWd5XEHpSUi6T9WpxuV_tcPCJ2FWINz92sJs68alU_CdXS98zPv_oPJEbdDhEEFKAKWs3NRU5ZRgu5g1&amp;t=638568676371266408" type="text/javascript"></script>
<script type="text/javascript">
//<![CDATA[
function WebForm_OnSubmit() {
if (typeof(ValidatorOnSubmit) == "function" && ValidatorOnSubmit() == false) return false;
return true;
}
//]]>
</script>

<div>

	<input type="hidden" name="__VIEWSTATEGENERATOR" id="__VIEWSTATEGENERATOR" value="A0C61021" />
</div>
        <div>
            <script type="text/javascript">
//<![CDATA[
Sys.WebForms.PageRequestManager._initialize('ctl00$scriptManager', 'aspnetForm', ['tctl00$ctl00$apMainAjaxPanelPanel','','tctl00$ctl00$apHelperAjaxPanelPanel',''], [], [], 600, 'ctl00');
//]]>
</script>

            
            
            
            <script type="text/javascript" language="javascript">
                var logger = log4javascript.getLogger("main");
                
                logger.info("*** Welcome to alfaRecordingsViewert client-side log ***");
            
                // make overlay more transparent
                $.blockUI.defaults.baseZ = 100001;
                $.blockUI.defaults.growlCSS.width = '480px';
                $.blockUI.defaults.growlCSS.opacity = 0.6;
                $.blockUI.defaults.overlayCSS.opacity = .4;
                                
                $.myGrowlUI = function(title, message, timeout, onClose) {
                    var $m = $('<div class="growlUI"></div>');
                    if (title) $m.append('<div style="font-size: 24px;">' + title + '</div>');
                    if (message) $m.append('<div>' + message + '</div>');
                    if (timeout == undefined) timeout = 2500;
                    $.blockUI({
                        message: $m, fadeIn: 100, fadeOut: 300, centerY: false,
                        timeout: timeout, showOverlay: false,
                        onUnblock: onClose,
                        css: {
                            width: '350px',
                            top: '32px',
                            left: '',
                            right: '10px',
                            border: 'solid 1px #AA4400',
                            padding: '5px',
                            opacity: 1.0,
                            cursor: 'default',
                            color: '#fff',
                            backgroundColor: '#FF9900',
                            '-webkit-border-radius': '10px',
                            '-moz-border-radius': '10px',
                            'border-radius': '10px'
                        }
                    });
                };
                
                // 
                if (!String.prototype.endsWith) {
                    
                    String.prototype.endsWith = function (suffix) {
                        return this.indexOf(suffix, this.length - suffix.length) !== -1;
                    };
                }
                
                function InitializeRequestHandler(sender, args)
                {
                    try {
                        if (Sys.WebForms.PageRequestManager.getInstance().get_isInAsyncPostBack()) {
                            /**/
                            $.myGrowlUI('Komunikacja z serwerem', 'Proszę czekać na zakończenie komunikacji z serwerem.');

                            // i anulujemy request
                            args.set_cancel(true);
                        }
                    } catch (e) {
                        logJSErrors(e);
                        alert('[InitializeRequestHandler] Wystąpił błąd: ' + e.message);
                    }
                }

                function BeginRequestHandler(sender, args) {
                    try {
                        // http://www.telerik.com/help/aspnet-ajax/ajxdisablecontrolsduringajax.html
                        // Disable the Button that Initiated Asynchronous PostBack Until Server Processing Completes in ASP.Net AJAX: http://www.codedigest.com/CodeDigest/40-Disable-the-Button-that-Initiated-Asynchronous-PostBack-Until-Server-Processing-Completes-in-ASP-Net-AJAX.aspx
                        postBackElement = args.get_postBackElement();
                        postBackElement.disabled = true;
                    }
                    catch (e) {
                        logJSErrors(e);
                        alert('[BeginRequestHandler] Wystąpił błąd: ' + e.message);
                    }
                }

                function EndRequestHandler(sender, args) {
                    try {
                        // http://www.codedigest.com/CodeDigest/40-Disable-the-Button-that-Initiated-Asynchronous-PostBack-Until-Server-Processing-Completes-in-ASP-Net-AJAX.aspx
                        postBackElement.disabled = false;

                        // http://msdn.microsoft.com/en-us/library/System.Web.UI.ScriptManager.OnAsyncPostBackError.aspx
                        if (args.get_error() != undefined && args.get_error().httpStatusCode == '500') {
                            
                            // Get error message
                            var errorMessage = args.get_error().message;
                            
                            // Setup onclick handler for error dialog button
                            $('#btnContinue').click(function() {
                                $.unblockUI();
                                return false;
                            });

                            // Setup exception details on error dialog
                            $get('divExceptionDetails').innerHTML = errorMessage;

                            // Show error dialog popup
                            $.blockUI({ message: $('#divException'), css: { width: '475px', border: '1px solid #565656'} });
                            /**/

                            // Stop error propagation
                            args.set_errorHandled(true);
                        }
                    }
                    catch (e) {
                        logJSErrors(e);
                        alert('[EndRequestHandler] Wystąpił błąd: ' + e.message);
                    }
                }

                function toggleErrorDetails() {
                    var divDetails = $get('divExceptionDetails');
                    var text = '';

                    if (divDetails.style.display == 'none') {
                        divDetails.style.display = '';
                        text = 'ukryj szczegóły błędu';
                    }
                    else {
                        divDetails.style.display = 'none';
                        text = 'pokaż szczegóły błędu';
                    }

                    $get('lnkDetails').innerHTML = text;
                }
            
                // INIT
                try {
                    var postBackElement;
                
                    var prm = Sys.WebForms.PageRequestManager.getInstance();
                    prm.add_initializeRequest(InitializeRequestHandler);
                    prm.add_beginRequest(BeginRequestHandler);
                    prm.add_endRequest(EndRequestHandler);      // http://weblogs.asp.net/davidbarkol/archive/2008/09/25/asynchronous-error-handling-change-in-asp-net-ajax-3-5.aspx
                }
                catch (e) {
                    logJSErrors(e);
                    alert('[Init] Wystąpił błąd: ' + e.message);
                }
                   
            </script>
            


            

            
            
            
            <div id="divException" style="padding: 8px; background-color: #ffffff; text-align: left; display: none;">
                <div style="border: solid 0px Black;">
                    <div style="background-color: #FFFBD1; border: solid 1px #808080; padding: 3px;">
                        <div class="bld" style="color: #EF3704; font-size: 24px; padding-bottom: 3px;">
                            <img id="ctl00_Image1" src="App_Themes/Alfavox/error.png" align="absmiddle" style="border-width:0px;" />Błąd
                        </div>
                        Wystąpił błąd podczas obsługi żądania wysłanego do serwera WWW. Proszę spróbować ponowić ostatnią akcję, a jeśli problem będzie dalej występował to należy skontaktować się z administratorem w celu przekazania szczegółów błedu dostępnych poniżej.
                    </div>
                    <br />
                    <a id="lnkDetails" href="javascript:void(0)" onclick="return toggleErrorDetails()" class="arrowBk floatRight" style="display: block;">pokaż szczegóły błędu</a>
                    <br />
                    
                    <div id="divExceptionDetails" style="background-color: #FFF5AD; border: solid 1px #808080; padding: 3px; margin-top: 3px; display: none; font-family: Tahoma; font-size: 11px; white-space: pre; overflow: scroll;"></div>
                    <br />
                    <input id="btnContinue" type="button" style="display: block; width: 86px;" class="btn floatRight" value="OK" />
                    
                    
                    <div style="clear: both;"></div>
                </div>
            </div>

            <div id="ctl00_pnlHead">
	
                <div id="headerWrapper">
                    <div id="headerContentWrapper" ondblclick="if (window && window.event && window.event.ctrlKey) alert('appName: ' + navigator.appName + '\nuserAgent: ' + navigator.userAgent + '\ndocumentMode: ' + document.documentMode + '\ncompatMode: ' + document.compatMode)">
                        <div class="floatLeft bld">
                            <a id="ctl00_hlMainPage" href="Default.aspx"><span id="ctl00_lblTopBarVersion" class="arrowBk">alfaRecordingViewer v19.7.0.309</span></a>&nbsp;
                            <span id="ctl00_lblTopBarBrowserMode" title="Detected browser defs: default;mozilla;webkit;chrome.
UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36" class="bld">@ Chrome v129.0+</span>
                        </div>
                        
                        
                        <a class="bld" href="ResetPassword.aspx?login=">Zmień hasło</a>
                        |
                        <a id="ctl00_lsLoginStatus" class="arrowBk bld" href="javascript:__doPostBack(&#39;ctl00$lsLoginStatus$ctl02&#39;,&#39;&#39;)">Zaloguj</a>
                    </div>
                </div>
            
</div>
      
            <div class="RadAjaxPanel" id="ctl00_ctl00_apMainAjaxPanelPanel">
	<div id="ctl00_apMainAjaxPanel" class="cbMain" style="border: solid 0px Black;">
		<!-- 2020.1.219.40 -->
                <div id="ctl00_alpMainLoadinPanel" class="RadAjax RadAjax_Default" style="display:none;height:100%;width:100%;">
			<div class="raDiv">
				
                    
                
			</div><div class="raColor raTransp">

			</div>
		</div>
             
                
                
                
                
                
    <script src="js/alfaCryptoJS/bundle.js"></script>
    <script>
        function generateHashAndLogin() {
            var login = $("#tbUser").val();
            var password = $("#tbPassword").val();
            if ($("#hiddenPBKDF2Enabled").val() === "True") {
                var hashed = window.alfaHash(login, password);
                $("#tbPassword").attr("disabled", true);
            }
            $("#hiddenHash").val(hashed);
            $("#btnLogin").click();
        }
    </script>
		<div class="contentBox" style="width: 350px; margin: auto; padding-top: 35px;">
			<div class="cbHeader">
				<div class="cbHeaderLeft">&nbsp;</div>
				<div class="cbHeaderBg arrowBk">Logowanie</div>
				<div class="cbHeaderRight">&nbsp;</div>
			</div>
			<div class="cbMain">
			    
			    
			    <div id="ctl00_cphMain_pnlLoginPanel">
			
    	            Aby uzyskać dostęp do aplikacji alfa Recordings Viewer należy zalogować się do systemu.
    	            <br />
    	            <br />
                    <table align="center" border="0">
	                    <tr>
		                    <td class="alignRight" valign="top">Użytkownik:</td>
		                    <td>
		                        <span id="tbUser_wrapper" class="riSingle RadInput RadInput_Default" style="width:160px;"><input id="tbUser" name="ctl00$cphMain$tbUser" size="20" maxlength="64" class="riTextBox riEnabled" type="text" value="" /><input id="tbUser_ClientState" name="tbUser_ClientState" type="hidden" /></span>
		                        <br />
                                <span id="ctl00_cphMain_rfvUser" style="color:Red;display:none;">Proszę uzupełnić.</span>
                            </td>
	                    </tr>
	                    <tr>
		                    <td class="alignRight" valign="top">Hasło:</td>
		                    <td>
		                        <span id="tbPassword_wrapper" class="riSingle RadInput RadInput_Default" style="width:160px;"><input id="tbPassword" name="ctl00$cphMain$tbPassword" size="20" maxlength="64" class="riTextBox riEnabled" type="password" /><input id="tbPassword_ClientState" name="tbPassword_ClientState" type="hidden" /></span>
		                        <br />
                                <span id="ctl00_cphMain_rfvPassword" style="color:Red;display:none;">Proszę uzupełnić.</span>
                            </td>
	                    </tr>
	                    <tr>
		                    <td colspan="2" class="alignRight">
                                <input type="hidden" name="ctl00$cphMain$hiddenPBKDF2Enabled" id="hiddenPBKDF2Enabled" value="False" />
		                        <input type="hidden" name="ctl00$cphMain$hiddenHash" id="hiddenHash" />
		                        <input type="button" name="ctl00$cphMain$btnReset" value="Reset" onclick="javascript:__doPostBack(&#39;ctl00$cphMain$btnReset&#39;,&#39;&#39;)" id="ctl00_cphMain_btnReset" class="btn wdth" />
		                        <input type="button" name="ctl00$cphMain$btnLoginHash" value="Zaloguj" onclick="generateHashAndLogin();WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions(&quot;ctl00$cphMain$btnLoginHash&quot;, &quot;&quot;, true, &quot;vgLogin&quot;, &quot;&quot;, false, true))" id="ctl00_cphMain_btnLoginHash" class="btn wdth" />
		                        <input type="button" name="ctl00$cphMain$btnLogin" value="Zaloguj" onclick="javascript:WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions(&quot;ctl00$cphMain$btnLogin&quot;, &quot;&quot;, true, &quot;vgLogin&quot;, &quot;&quot;, false, true))" id="btnLogin" class="btn wdth" style="display: none" />
		                        
		                    </td>
	                    </tr>
                    </table>
                
		</div>
                
                <span id="ctl00_cphMain_lblMessage" style="color:Red;"></span>
            </div>
			<div class="cbFooter">
				<div class="cbFooterLeft">&nbsp;</div>
				<div class="cbFooterBg">&nbsp;</div>
				<div class="cbFooterRight">&nbsp;</div>
			</div>
        </div>


            
	</div>
</div>
        </div>
        <div class="RadAjaxPanel" id="ctl00_ctl00_apHelperAjaxPanelPanel">
	<div id="ctl00_apHelperAjaxPanel">

	</div>
</div>
        
        
        <img src="App_Themes/Alfavox/icon-working-12x12_bk_gray.gif" style="visibility: hidden;" />
        <img src="App_Themes/Alfavox/icon-working-12x12_bk_transparent.gif" style="visibility: hidden;" />
    
<script type="text/javascript">
//<![CDATA[
var Page_Validators =  new Array(document.getElementById("ctl00_cphMain_rfvUser"), document.getElementById("ctl00_cphMain_rfvPassword"));
//]]>
</script>

<script type="text/javascript">
//<![CDATA[
var ctl00_cphMain_rfvUser = document.all ? document.all["ctl00_cphMain_rfvUser"] : document.getElementById("ctl00_cphMain_rfvUser");
ctl00_cphMain_rfvUser.controltovalidate = "tbUser";
ctl00_cphMain_rfvUser.errormessage = "RequiredFieldValidator";
ctl00_cphMain_rfvUser.display = "Dynamic";
ctl00_cphMain_rfvUser.validationGroup = "vgLogin";
ctl00_cphMain_rfvUser.evaluationfunction = "RequiredFieldValidatorEvaluateIsValid";
ctl00_cphMain_rfvUser.initialvalue = "";
var ctl00_cphMain_rfvPassword = document.all ? document.all["ctl00_cphMain_rfvPassword"] : document.getElementById("ctl00_cphMain_rfvPassword");
ctl00_cphMain_rfvPassword.controltovalidate = "tbPassword";
ctl00_cphMain_rfvPassword.errormessage = "RequiredFieldValidator";
ctl00_cphMain_rfvPassword.display = "Dynamic";
ctl00_cphMain_rfvPassword.validationGroup = "vgLogin";
ctl00_cphMain_rfvPassword.evaluationfunction = "RequiredFieldValidatorEvaluateIsValid";
ctl00_cphMain_rfvPassword.initialvalue = "";
//]]>
</script>


<script type="text/javascript">
//<![CDATA[
window.__TsmHiddenField = $get('ctl00_scriptManager_TSM');
var Page_ValidationActive = false;
if (typeof(ValidatorOnLoad) == "function") {
    ValidatorOnLoad();
}

function ValidatorOnSubmit() {
    if (Page_ValidationActive) {
        return ValidatorCommonOnSubmit();
    }
    else {
        return true;
    }
}
        ;(function() {
                        function loadHandler() {
                            var hf = $get('ctl00_RadStyleSheetManager1_TSSM');
                            if (!hf._RSSM_init) { hf._RSSM_init = true; hf.value = ''; }
                            hf.value += ';Telerik.Web.UI, Version=2020.1.219.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:pl-PL:d010718b-d2d4-4e34-a63a-374109c08bc7:45085116:27c5704c:aac1aeb7:c73cf106';
                            Sys.Application.remove_load(loadHandler);
                        };
                        Sys.Application.add_load(loadHandler);
                    })();WebForm_AutoFocus('tbUser');Sys.Application.add_init(function() {
    $create(Telerik.Web.UI.RadAjaxLoadingPanel, {"initialDelayTime":0,"isSticky":false,"minDisplayTime":150,"skin":"Default","uniqueID":"ctl00$alpMainLoadinPanel","zIndex":90000}, null, null, $get("ctl00_alpMainLoadinPanel"));
});
Sys.Application.add_init(function() {
    $create(Telerik.Web.UI.RadTextBox, {"_displayText":"","_focused":true,"_initialValueAsText":"","_postBackEventReferenceScript":"setTimeout(\"__doPostBack(\\\u0027ctl00$cphMain$tbUser\\\u0027,\\\u0027\\\u0027)\", 0)","_skin":"Default","_validationGroup":"vgLogin","_validationText":"","clientStateFieldID":"tbUser_ClientState","enabled":true,"styles":{HoveredStyle: ["width:160px;", "riTextBox riHover"],InvalidStyle: ["width:160px;", "riTextBox riError"],DisabledStyle: ["width:160px;", "riTextBox riDisabled"],FocusedStyle: ["width:160px;", "riTextBox riFocused"],EmptyMessageStyle: ["width:160px;", "riTextBox riEmpty"],ReadOnlyStyle: ["width:160px;", "riTextBox riRead"],EnabledStyle: ["width:160px;", "riTextBox riEnabled"]}}, null, null, $get("tbUser"));
});

document.getElementById('ctl00_cphMain_rfvUser').dispose = function() {
    Array.remove(Page_Validators, document.getElementById('ctl00_cphMain_rfvUser'));
}
Sys.Application.add_init(function() {
    $create(Telerik.Web.UI.RadTextBox, {"_focused":false,"_postBackEventReferenceScript":"setTimeout(\"__doPostBack(\\\u0027ctl00$cphMain$tbPassword\\\u0027,\\\u0027\\\u0027)\", 0)","_skin":"Default","_validationGroup":"vgLogin","clientStateFieldID":"tbPassword_ClientState","enabled":true,"styles":{HoveredStyle: ["width:160px;", "riTextBox riHover"],InvalidStyle: ["width:160px;", "riTextBox riError"],DisabledStyle: ["width:160px;", "riTextBox riDisabled"],FocusedStyle: ["width:160px;", "riTextBox riFocused"],EmptyMessageStyle: ["width:160px;", "riTextBox riEmpty"],ReadOnlyStyle: ["width:160px;", "riTextBox riRead"],EnabledStyle: ["width:160px;", "riTextBox riEnabled"]}}, null, null, $get("tbPassword"));
});

document.getElementById('ctl00_cphMain_rfvPassword').dispose = function() {
    Array.remove(Page_Validators, document.getElementById('ctl00_cphMain_rfvPassword'));
}
Sys.Application.add_init(function() {
    $create(Telerik.Web.UI.RadAjaxPanel, {"clientEvents":{OnRequestStart:"",OnResponseEnd:""},"enableAJAX":true,"enableHistory":false,"links":[],"loadingPanelID":"ctl00_alpMainLoadinPanel","styles":[],"uniqueID":"ctl00$apMainAjaxPanel"}, null, null, $get("ctl00_apMainAjaxPanel"));
});
Sys.Application.add_init(function() {
    $create(Telerik.Web.UI.RadAjaxPanel, {"clientEvents":{OnRequestStart:"",OnResponseEnd:""},"enableAJAX":true,"enableHistory":false,"links":[],"loadingPanelID":"","styles":[],"uniqueID":"ctl00$apHelperAjaxPanel"}, null, null, $get("ctl00_apHelperAjaxPanel"));
});
//]]>
</script>
</form>
</body>
</html>
"""


def test_parse_form_values(body):
    page = HtmlPage(body)

    form = next(page.find_all_forms())
    act = form.get_values()
    
    assert "Zaloguj" == act["ctl00$cphMain$btnLoginHash"]
