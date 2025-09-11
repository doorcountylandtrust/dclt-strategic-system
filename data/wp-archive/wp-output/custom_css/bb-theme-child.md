# bb-theme-child

*Date:* 2023-01-25 14:12:48
*Author:* dcltadmin
*Link:* https://www.doorcountylandtrust.org/bb-theme-child/

/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
Custom Print Stylesheet
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*/
@media print{ header, nav, .fl-menu, .shiftnav, #sidebar-menu, .sidebar-menu, .fl-row-bg-photo, .fl-separator, button, footer{
display: none;
}
}
/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
Custom Gravity PDF Button
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*/
a.gravitypdf-download-link {
color: white;
background-color: #547c57;
padding: 10px;
border-radius: 15px;
}
/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
Custom Google Maps
Preserves Listings Titles
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*/
p.wpgmza\_infowindow\_title {
font-size: 20px;
color: #004731;
}
/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
Custom Google Maps (Desktop)
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*/
.wpgmza-inner-stack.left {
margin-top: 30px;
margin-bottom: 0;
max-width: 32% !important;
}
.wpgmza\_map .wpgmza-inner-stack .legacy-listing-adapter .wpgmaps\_blist\_row {
padding: 5px !important;
}
.wpgmza-pagination {
display: none;
}
.wpgmaps-preserves-listings-heading h1 {
width: 100%;
margin: 0;
padding: 5px 15px;
font-size: 24px !important;
font-weight: bold;
text-transform: uppercase;
color: white;
background-color: #2c6652;
}
/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
Custom Google Maps (Mobile)
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*/
/\* HTML/JS Element \*/
div#wpgmza-outer-stack .fl-module-content.fl-node-content {
margin-top: -30px;
}
.wpgmaps-mobile-preserves-listings {
font-size: 22px;
line-height: 22px;
font-weight: bold;
margin-top: -40px 20px 10px 20px;
pointer-events: all;
color: #2c6652;
}
.wpgmaps-mobile-preserves-listings .fl-heading-text {
background-color: #2c6652;
color: white;
display: block;
width: 100vw;
margin-top: -50px;
margin-left: -20px;
padding-left: 10px;
}
.wpgmaps-mobile-preserves-listings .wpgmza-inner-stack.left {
margin-top: 40px;
}
.wpgmaps-mobile-preserves-listings .wpgmza-inner-stack.left {
max-width: 100% !important;
}
.wpgmaps-mobile-preserves-listings .wpgmza-basic-list-item {
display: block;
margin-top: 0;
padding-left: 10px;
padding-bottom: 20px;
}
.wpgmaps-mobile-preserves-listings:hover {
cursor: pointer;
}
/\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
Formstack embeds
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*
\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*/
button.fsSubmitButton {
background-color: #547c57;
color: #fff;
line-height: 1.2;
padding: 6px 12px;
font-weight: normal;
text-shadow: none;
border: 1px solid #3b583d;
-moz-box-shadow: none;
-webkit-box-shadow: none;
box-shadow: none;
-moz-border-radius: 4px;
-webkit-border-radius: 4px;
border-radius: 4px;
}
.SStyledReferralBadge-sc-5yap1m-0, .xqtmq {
display:none;
}