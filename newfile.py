from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import TwoLineAvatarIconListItem, TwoLineAvatarListItem, ImageLeftWidget, ILeftBodyTouch, IRightBodyTouch
from kivymd.uix.label import MDLabel
from kivymd.color_definitions import colors
from kivymd.uix.behaviors import BackgroundColorBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import RoundedRectangle, Color
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivy.lang import Builder
from PIL import Image
import mysql.connector as mc
from datetime import datetime, date
import re
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import StringProperty, ListProperty,ObjectProperty, NumericProperty, AliasProperty, BooleanProperty, OptionProperty
from kivy.clock import Clock
from kivy.core.window import Window
Window.softinput_mode = 'below_target'

from photogallery import Gallery, CustomGallerySheet, PhotoCropper, EditDialog

Builder.load_string('''
#: import rgba kivy.utils.get_color_from_hex
#: import ScrollEffect kivy.effects.scroll.ScrollEffect


<LoginScreen>:
	Screen:
		name: 'login'
		
		RelativeLayout:
			canvas:
				Color:
					rgba: app.theme_cls.primary_color
				RoundedRectangle:
					size: self.width, self.height*5/3
					pos: 0, self.height/3.5
					radius: (0, 0, 50, 50)
					
			MDCard:
				canvas:
					Color:
						rgba: app.theme_cls.primary_color
					RoundedRectangle:
						size: self.width-10, self.height/5
						pos: (root.width/2 - self.width/2)+5, (root.height/3.5)
						radius: (100, 100, 0, 0)
				size_hint: None, None
				size: 500, 900
				pos_hint: {'center_x':0.5, 'center_y': 0.6}
				orientation: 'vertical'
				
				MDFloatingActionButton:
					icon:'window-close'
					md_bg_color: app.theme_cls.primary_color
					pos_hint: {'center_x': 0.88, 'center_y': 0.1}
					on_release: app.stop()
					
				MDLabel:
					markup: True
					text: "[i][size=32]SIGN IN[/size][/i]"
					color: app.theme_cls.primary_color
					halign: 'center'
					
				MDLabel:
					id: log_error_mes
					markup: True
					text: ''
					size_hint_y: 0.2
					halign: 'center'
					
				#username					
				LTextField:
					id: username
					hint_text: "Username or Email"
					max_text_length: 30
					text_color: app.theme_cls.primary_color
					
				#password
				BoxLayout:
					size_hint: 0.85, None
					height: password.height
					pos_hint: {'center_x': 0.5}
					LTextField:
						id: password
						hint_text: "Password"
						password: True
						text_color: app.theme_cls.primary_color
					MDIconButton:
						id: see_password
						icon: 'eye'
						theme_text_color: 'Custom'
						text_color: app.theme_cls.primary_color
						on_press: root.switch_seen()
						
					
				Label:
					size_hint_y: 0.25
					
				MDFillRoundFlatIconButton:
					id: login
					text: 'Sign In'
					text_color: app.theme_cls.primary_color
					theme_text_color: 'Custom'
					icon_color: app.theme_cls.primary_color
					md_bg_color: app.theme_cls.bg_light
					size_hint_x: 0.7
					pos_hint: {'center_x': 0.5}
					on_release: root.login()
					
				MDRectangleFlatButton:
					id: signup
					text: 'Sign Up'
					text_color: app.theme_cls.bg_light
					size_hint_x: 0.5
					pos_hint: {'center_x': 0.5}
					on_release: root.current = 'register'
					
				Label:
					size_hint_y: 0.13	
					
			Label:
				text: ''

###########******************############
#                       Registration Page                           #
####################################

	Screen:
		name: 'register'
		RelativeLayout:
			canvas:
				Color:
					rgba: app.theme_cls.primary_color
				RoundedRectangle:
					size: self.width, self.height/2
					pos: 0, self.height/2
					radius: (0, 0, 50, 50)
			MDCard:
				canvas:
					Color:
						rgba: app.theme_cls.primary_color
					Rectangle:
						size: self.width-10, self.height/3
						pos: (root.width/2 - self.width/2)+5, (root.height/2-self.height/3)
				size_hint: None, None
				size: 500, 1000
				pos_hint: {'center_x': 0.5, 'center_y': 0.6}
				orientation: 'vertical'
				MDFloatingActionButton:
					icon:'window-close'
					md_bg_color: app.theme_cls.primary_color
					pos_hint: {'center_x': 0.88, 'center_y': 0.1}
					on_release: app.stop()
					
				MDLabel:
					markup: True
					text: "[i][size=32]SIGN UP[/size][/i]"
					color: app.theme_cls.primary_color
					halign: 'center'
					size_hint_y: 0.1
							
				MDLabel:
					id: reg_error_mes
					markup: True
					text: ''
					size_hint_y: 0.2
					halign: 'center'
							
				ScreenManager:
					id: reg_step
					size_hint: None, None
					size: 500, 500
					
					Screen:
						name: 'first_reg_page'
						BoxLayout:
							size_hint: 0.85, None
							orientation: 'vertical'
							
							#full name
							LTextField:
								id: reg_firstname
								hint_text: "First Name"
								max_text_length: 20
								text_color: app.theme_cls.primary_color
									
							LTextField:
								id: reg_surname
								hint_text: "SurName"
								max_text_length: 20
								text_color: app.theme_cls.primary_color
								
					Screen:
						name: 'second_reg_page'
						BoxLayout:
							size_hint: 0.85, None
							orientation: 'vertical'
							
							#Date of Birth
							BoxLayout:
								size_hint_x: .7
								pos_hint: {'x': .15}
							    MDDropDownItem:
							    	id: year
							    	items: root.year()
							    	text_color: app.theme_cls.primary_color
							    	dropdown_bg: app.theme_cls.primary_color
							    MDDropDownItem:
							    	id: month
							    	items: root.month()
							    	text_color: app.theme_cls.primary_color
							    	dropdown_bg: app.theme_cls.primary_color
							    MDDropDownItem:
							    	id: day
							    	items: root.day(month.current_item, year.current_item)
							    	text_color: app.theme_cls.primary_color
									dropdown_bg: app.theme_cls.primary_color
							Label:
								size_hint_y: 1
							
							#gender
							MDDropDownItem:
					 	   	id: gender
						    	items: ['', 'Male', 'Female', 'Custom']
						    	text_color: app.theme_cls.primary_color
						    	pos_hint: {'x': .15}
						    	dropdown_bg: app.theme_cls.primary_color
						    Label:
								size_hint_y: .2
								
					Screen:
						name: 'third_reg_page'
						BoxLayout:	
							size_hint: 0.85, None
							orientation: 'vertical'
							
							#username					
							LTextField:
								id: reg_username
								hint_text: "Username"
								max_text_length: 20
								text_color: app.theme_cls.primary_color
								
							#email
							LTextField:
								id: reg_email
								hint_text: "Email"
								max_text_length: 30
								text_color: app.theme_cls.primary_color
					
					Screen:
						name: 'fourth_reg_page'
						BoxLayout:
							size_hint: 0.85, None
							orientation: 'vertical'
							
							#password					
							BoxLayout:
								size_hint: 0.85, None
								height: reg_password.height
								pos_hint: {'center_x': 0.5}
								LTextField:
									id: reg_password
									hint_text: "Password"
									password: True
									text_color: app.theme_cls.primary_color
								MDIconButton:
									id: see_reg_password
									icon: 'eye'
									theme_text_color: 'Custom'
									text_color: app.theme_cls.primary_color
									on_press: root.switch_seen2()
									
							LTextField:
								id: check_password
								hint_text: "Retype Password"
								password: True
								text_color: app.theme_cls.primary_color
					
				Label:
					size_hint_y: 15
					
				MDFillRoundFlatIconButton:
					id: login
					text: 'Next'
					text_color: app.theme_cls.primary_color
					md_bg_color: app.theme_cls.bg_light
					size_hint_x: 0.7
					pos_hint: {'center_x': 0.5}
					on_release: root.switch_reg_page()
					
				MDRectangleFlatButton:
					id: signup
					text: 'Have An Account Already'
					text_color: app.theme_cls.bg_light
					size_hint_x: 0.8
					pos_hint: {'center_x': 0.5}
					on_release: root.current = 'login'
					
				Label:
					size_hint_y: 10
					
			Label:
				text: ''

###########******************############
#                       Main App Screen                          #
####################################

		
#: import SwapTransition kivy.uix.screenmanager.SwapTransition
#:import colors kivymd.color_definitions.colors
<AppScreen>:
	
	NavigationLayout:
		ScreenManager:
			id: appscreen
			Screen:
				name: 'mainscreen'
				BoxLayout:
					orientation: 'vertical'
					
					MDToolbar:
						title: '         SmartChat'
						md_bg_color: app.theme_cls.primary_color
						left_action_items: [['menu',lambda x: nav_drawer.set_state('open')]]
						size_hint_y: None
						height: dp(45)
						
					BoxLayout:
						orientation: 'vertical'
						
						ScreenManager:
							id: switch
							transition: SwapTransition(duration= 0.2)
							Screen:
								name: 'chat'
								ScrollView:
									id: refresh_friends_list
									MDList:
										id: chatter_page
										spacing: dp(20)
										MDLabel:
											text: "No Active Chat"
											font_size: 72
											size_hint: 1, None
											height: self.width
											theme_text_color: 'Custom'
											text_color: app.theme_cls.primary_color
											halign: 'center'
											valign: 'bottom'
										MDRectangleFlatButton:
											text: 'Friends'
											size_hint: 1, None
											height: dp(40)
											on_press:
												root.open_profile('friends')
												
											
									
								
							Screen:
								name: 'search'
								BoxLayout:
									orientation: 'vertical'
									
									BoxLayout:
										size_hint_y: None
										height: search_peo.height*1.5
										Label:
											size_hint_x: None
											width: dp(50)
										MDTextField:
								    		id: search_peo
								    		mode: 'line'
								    		active_color: app.theme_cls.primary_light
								    		theme_text_color: 'Custom'
								    		icon_right: 'search'
								    		
											
											on_text: root.search_item(self.text.lower(), True)
											size_hint_x: None
											width: 500
										MDIconButton:
											icon: 'magnify'
											
									ScrollView:
										
										MDList:
											id: search_view
											padding: dp(20)
											spacing: dp(10)
											default_size: None, dp(48)
											default_size_hint: 1, None
											size_hint_y: None
											height: self.minimum_height
									
									
							Screen:
								name: 'games'
								
						BoxLayout:
							size_hint_y: None
							height: dp(40)
							MDRectangleFlatIconButton:
								text: "Chat"
								icon: 'chat'
								md_bg_color: app.theme_cls.primary_color
								text_color: app.theme_cls.primary_light
								on_press: switch.current = 'chat'
								size_hint_x: .3
							MDRectangleFlatIconButton:
								text: "Search"
								icon: 'magnify'
								md_bg_color: app.theme_cls.primary_color
								text_color: app.theme_cls.primary_light
								on_press: switch.current = 'search'
								size_hint_x: .3
							MDRectangleFlatIconButton:
								text: "Games"
								icon: 'gamepad-variant'
								md_bg_color: app.theme_cls.primary_color
								text_color: app.theme_cls.primary_light
								on_press: switch.current = 'games'
								size_hint_x: .3
								
							
		MDNavigationDrawer:
			id: nav_drawer
			canvas:
				Color:
					rgba: app.theme_cls.primary_dark
				Rectangle:
					size: self.size
					pos: self.pos
					
			BoxLayout:
				size_hint: 1, None
				height: nav_drawer.height
				orientation: 'vertical'
				padding: (dp(20), dp(20), dp(20), dp(20))
				
				RelativeLayout:
					id: top_profile
					size_hint: 1, None
					height: self.width
					
					MDIconButton:
						icon: 'backburger'
						on_press: nav_drawer.set_state('close')
						pos_hint: {'x': .8, 'y': .9}
						
					ProfileImage:
						size_hint: 0.5, None
						height: self.width
						pos_hint: {'x': .05, 'y' : .5}
						canvas:
							Color:
								rgba: rgba('#ffffff')
							RoundedRectangle:
								source: 'icon.png'
								size: self.width, self.width
								radius: (self.width/2,self.width/2,self.width/2,self.width/2)
								
					Label:
						markup: True
						id: full_name
						font_family: 'serif'
						pos_hint: {'x' : -0.2, 'y': -0.05}
						
					Label:
						markup: True
						id: user_name
						font_family: 'serif'
						pos_hint: {'x' : -0.25, 'y': -0.15}
						
					Label:
				ScrollView:
					effect_cls: ScrollEffect
					MDList:
						
						NavList:
							text: 'Home'
							on_release:
								nav_drawer.set_state('close')
								appscreen.current = 'mainscreen'
							IconLeftWidget:
								md_bg_color: app.theme_cls.primary_light
								icon: 'settings-outline'
								
						NavList:
							text: 'Profile'
							on_release: root.open_profile()
							IconLeftWidget:
								md_bg_color: app.theme_cls.primary_light
								icon: 'settings-outline'
						
						OneLineListItem:
							height: dp(20)
							
						NavList:
							text: 'Settings'
							IconLeftWidget:
								md_bg_color: app.theme_cls.primary_light
								icon: 'settings-outline'
						
						NavList:
							text: 'Settings'
							IconLeftWidget:
								md_bg_color: app.theme_cls.primary_light
								icon: 'settings-outline'
						
						NavList:
							text: 'Settings'
							on_release: root.open_setting()
							
							IconLeftWidget:
								md_bg_color: app.theme_cls.primary_light
								icon: 'settings-outline'
								
						OneLineListItem:
							height: dp(20)
								
						NavList:
							text: 'Account Settings'
							IconLeftWidget:
								md_bg_color: app.theme_cls.primary_light
								icon: 'settings-outline'
								
						NavList:
							text: 'Sign Out'
							on_release: root.log_out()
							IconLeftWidget:
								md_bg_color: app.theme_cls.primary_light
								icon: 'settings-outline'
								
						NavList:
							text: 'Exit'
							on_release: app.stop()
							IconLeftWidget:
								md_bg_color: app.theme_cls.primary_light
								icon: 'settings-outline'
			
		MDNavigationDrawer:
			id: log_drawer
			md_bg_color: rgba(root.acolor)
			anchor: 'right'

<NavList@OneLineIconListItem+ButtonBehavior>:
	height: dp(60)
	theme_text_color: 'Custom'
	text_color: rgba('#ffffff')


######SEARCH ITEM AND OTHERS########
	
<SearchItem>:
	cols: 1
	TwoLineAvatarIconListItem:
		id: details
		text: ''
		secondary_text: ''
		SearchLeftWidget:
			canvas:
				RoundedRectangle:
					source: root.image()
					pos: self.pos
					size: self.height, self.height
					radius: (self.height/2,self.height/2,self.height/2, self.height/2)
					
		SearchIconWidget:
			id: lefticon
			icon: 'chevron-right'
			on_press:
				root.toggle_view()
					
				
					

<SearchLeftWidget@ILeftBodyTouch+BoxLayout>

<SearchIconWidget@IRightBodyTouch+MDIconButton>

<SearchItemContent>:
	cols: 3
	MDRectangleFlatIconButton:
		text: "Send Request"
		icon: 'account-plus'
		md_bg_color: app.theme_cls.primary_color
		text_color: app.theme_cls.primary_light
		size_hint_x: None
		width: root.width/10*4.5
		
	MDRectangleFlatIconButton:
		text: "View Profile"
		icon: 'account-details'
		md_bg_color: app.theme_cls.primary_color
		text_color: app.theme_cls.primary_light
		size_hint_x: None
		width: root.width/10*4.5
		
	MDRectangleFlatIconButton:
		icon: 'close-box'
		md_bg_color: app.theme_cls.primary_color
		text_color: app.theme_cls.primary_light
		size_hint_x: None
		width: root.width/10*1

####################################

		
<ProfileTab@MDTabsBase+RelativeLayout>:
	md_bg_color: app.theme_cls.primary_color
<ProfileTop@BoxLayout+BackgroundColorBehavior>

<ProfileImage@RelativeLayout+ButtonBehavior>:
	size_hint: None, None
	size: dp(200), dp(200)

<ProfilePage>:
	BoxLayout:
		orientation: 'vertical'
		
		ProfileTop:
			md_bg_color: app.theme_cls.primary_color
			size_hint_y: .5
			
			RelativeLayout:
				TextWidget:
					id: profile_pic
					text: 'icon.png'
				ProfileImage:
					pos_hint: {'center_x': 0.375, 'center_y': 0.425}
					canvas:
						Color:
							rgba: rgba('#bbbbbb')
						RoundedRectangle:
							source: profile_pic.text
							pos: self.pos
							size: self.size
							radius: dp(100), dp(100), dp(100), dp(100)	
					on_release:
						root.set_profile_pic()
				MDIconButton:
					icon: 'account-convert'
					pos_hint: {'center_x': 0.65, 'center_y': 0.75}
					on_press: root.change_profile_pic()
					
		MDTabs:
			id: details
			tab_indicator_anim: True
			md_bg_color: app.theme_cls.primary_color
			ProfileTab:
				text: 'Profile'
				BoxLayout:
					orientation: 'vertical'
					ScrollView:
						MDList:
							
			
			ProfileTab:
				text: 'Friends'
				BoxLayout:
					orientation: 'vertical'
					
			ProfileTab:
				text: 'Time Line'
				BoxLayout:
					orientation: 'vertical'
					

<ChatPage>:
		
	GridLayout:
		id: page_layout
		cols: 1
		MDToolbar:
			id: toolbar
			size_hint_y: None
			height: dp(45)
			left_action_items: [['backburger',lambda x: root.goback()]]
		ScrollView:
			BoxLayout:
				id: message_history
				Label:
					text: 'chat'
									
		BoxLayout:
			size_hint_y: None
			height: message.height
			MDIconButton:
				icon: 'image'
				theme_text_color: "Custom"
				text_color: app.theme_cls.primary_color
					
			MDIconButton:
				icon: 'microphone'
				theme_text_color: "Custom"
				text_color: app.theme_cls.primary_color
				
			Label:
				size_hint_x: None
				width: dp(10)
				
			MDTextField:
				id: message
				mode: 'fill'
				fill_color: rgba('#ffffff')
				size_hint: None, None
				size: dp(180), dp(30)
				font_size: 35
				font_family: 'serif'
				theme_line_color: "Custom"
				line_color:  app.theme_cls.primary_color
			Label:
				
			MDIconButton:
				icon: 'send'
				theme_text_color: "Custom"
				text_color:  app.theme_cls.primary_color
				on_press:
					root.send_message()
				
		Label:
			size_hint_y: None
			height: dp(10)


<CustomSwitch@MDI+IRightBodyTouch>

<SettingListItem@OneLineIconListItem+ButtonBehavior>

<AppSetting>:
	ScrollView:
		MDList:
			SettingListItem:
				on_release:
					app.theme_cls.theme_style = 'Light'
					
			SettingListItem:
				on_release:
					app.theme_cls.theme_style = 'Dark'
					
			SettingListItem:
				on_release:
					app.theme_cls.primary_palette= 'Teal'
					
			SettingListItem:
				on_release:
					app.theme_cls.primary_palette= 'LightGreen'
				
<LLoader>:
	MDIconButton:
		id: reload
		icon: 'reload'
		pos_hint: {'center_x': .5, 'center_y': .5}
		on_press:
			spinner.active = True
			self.icon= 'reload-alert'
			root.acive = False
			
					
	MDSpinner:
		id: spinner
		size_hint: None, None
		size: dp(30), dp(30)
		pos_hint: {'center_x': .5, 'center_y': .5}
		active: False

	
		
	
<PictureCard>:
	size_hint: None, None
	size: 500, 1000
	Image
		source: 'icon.png'
	
	
			
<LTextField@MDTextField>:
	required: True
	helper_text_mode: 'on_error'
	pos_hint: {'center_x': 0.5}
	size_hint_x: 0.85
	theme_text_color: 'Custom'
	pos_hint: {'center_x': 0.5}
''')


####################################
#                 MAIN APP SCREEN                              #
####################################

	
class AppScreen(Screen):
	bcolor = '#b2c95e'
	acolor = '#ffffff'
	
	custom_sheet = None
	
	def __init__(self, conn ='', user ='', user_id ='', **kwargs):
		super(AppScreen, self).__init__(**kwargs)
		
		self.mydb = conn
		self.user = user
		self.user_id = user_id
		self.getdetails()
		self.chatpage()
		
	def getdetails(self):
		self.appcursor = self.mydb.cursor()
		query = "SELECT first_name, surname, username FROM profile WHERE (username =%s or email =%s) and profile_id = %s"
		self.appcursor.execute(query, (self.user, self.user, str(self.user_id),))
		
		fname, sname, self.uname = self.appcursor.fetchone()
		self.fullname = (fname.capitalize() + " " + sname.capitalize())
		self.setprofile()
		
	
			
	def setprofile(self):
		self.ids['full_name'].text = "[b][size=42]{}[/size][/b]".format(self.fullname)
		self.ids['user_name'].text = "[i][size=32]@{}[/size][/i]".format(self.uname)

	
							
	def open_profile(self, detail='profile'):
		profilepage = ProfilePage(name='myprofile',details=detail, user= self.uname, conn= self.mydb)
		self.ids['appscreen'].add_widget(profilepage)
		self.ids['nav_drawer'].set_state('close')
		self.ids['appscreen'].current = 'myprofile'
		
		
	def open_setting(self):
		appsetting = AppSetting(name = 'appsetting')
		self.ids['appscreen'].add_widget(appsetting)
		self.ids['nav_drawer'].set_state('close')
		self.ids['appscreen'].current = 'appsetting'
		
	
			
	def chatpage(self):
		chatter_page = self.ids['chatter_page']
		self.listed = 0
		mycursor = self.mydb.cursor()
		
		mycursor.execute("SELECT 'from', 'to', 'message', 'time' FROM messages WHERE 'from' = %s or 'to' = %s", (self.user, self.user))
		
		results = mycursor.fetchall()
		self.messagers = []
		self.messages = []
		
		for chatter in results:
			sender, receiver, message, time = chatter
			if sender == user or  receiver == user:
				if sender == user:
					self.messagers.append(receiver)
				elif receiver == user:
					self.messagers.append(sender)
		
				mescursor = self.mydb.cursor
				newquery = 'SELECT first_name, surname, profile_pic FROM profiles WHERE (username = %s)or(username = %s)'
				
		if not (self.messagers == []):
			chatter_page.clear_widgets()
			
			for i in self.messagers[:10]:
				chatter_item = ChatListItem(text= self.fullname, secondary_text= "name: {}".format(str(i)), chat='chat{}'.format(i), size_hint_y=None, height=300, conn= self.mydb)
				chatter_item.add_widget(PicLeftWidget(pic='icon.jpg'))
				
				chatter_page.add_widget(chatter_item)
			
			lloader = LLoader(size_hint_y= None, height= 100)	
			chatter_page.add_widget(lloader)
		
		
		
	def search_item(self, text='', search=False):
		search_cursor = self.mydb.cursor()
		query = " SELECT first_name, surname, username FROM profile "
		search_cursor.execute(query)
		search_result = search_cursor.fetchall()
		
		def add_search_item(names):
			
			sfname, ssname, suname = names
			sfull_name = sfname.capitalize()+" "+ssname.capitalize()
			
			self.ids['search_view'].add_widget(
			SearchItem(
				text= sfull_name,
				user = suname,
				conn = self.mydb,
				height = 150
				)
			)
			
		self.ids['search_view'].clear_widgets()
		for names in search_result:
			
			fname, sname, uname = names
			full_name = fname+" "+sname
			uname = '@'+uname
			
			if search:
				if text == '':
					output='nothing to output'
				elif text == '@':
					output='nothing to output'
				elif text in full_name:
					add_search_item(names)
				elif '@' in text and text in uname:
					add_search_item(names)
					
					
		
	def log_out(self):
		loginscreen = LoginScreen(conn =self.mydb)
		signin = Screen(name='loginpage')
		signin.add_widget(loginscreen)
		self.parent.add_widget(signin)
		file = open('save.data','w')
		file.write('')
		self.parent.current = 'loginpage'
		self.parent.remove_widget(self)
			
			
			
			
class PicLeftWidget(ILeftBodyTouch, RelativeLayout):
	def __init__(self, pic='', **kwargs):
		super(PicLeftWidget, self).__init__(**kwargs)
		h, w = self.height/2,  self.width/2
		with self.canvas:
			RoundedRectangle(pos = self.pos, size = (h*2, w*2), source = pic, radius= (h, h, h, h))




#####SEARCH ITEMS IN SEARCH PAGE#####

class SearchItem(GridLayout):
	pic = 'icon.png'
	toggle = False
	
	def __init__(self, text, user, conn, **kwargs):
		super(SearchItem, self).__init__(**kwargs)
		
		self.user = user
		self.mydb = conn
		self.pic = 'icon.png'
		
		self.ids['details'].text = text
		self.ids['details'].secondary_text = user
		
		self.size_hint_y= None
		self.height = 150
		
	def image(self):
		return self.pic
		
	def toggle_view(self):
		content = SearchItemContent(user = self.user, conn = self.mydb, rows= 2, height=100, size_hint_y= None)
		
		details = self.ids['details']
		
		if not self.toggle:
			self.ids['lefticon'].icon='chevron-down'
			self.height = 250
			self.add_widget(content)
			self.toggle = True
		else:
			self.ids['lefticon'].icon='chevron-right'
			self.height = 150
			self.clear_widgets()
			self.add_widget(details)
			self.toggle = False
		
		
class SearchItemContent(GridLayout):
	def __init__(self, user, conn, **kwargs):
		super(SearchItemContent, self).__init__(**kwargs)

####################################


class PictureCard(MDCard):
	def __init__(self, source= '', **kwargs):
		super(PictureCard,self).__init__(**kwargs)
		

			
class LLoader(RelativeLayout):
	active = False
	def __init__(self, **kwargs):
		super(LLoader, self).__init__(**kwargs)
		
		

		
class AppSetting(Screen):
	def __init__(self, **kwargs):
		super(AppSetting, self).__init__(**kwargs)
	
	
class ChatListItem(TwoLineAvatarIconListItem, ButtonBehavior):
	def __init__(self, chat, conn, **kwargs):
		super(ChatListItem, self).__init__(**kwargs)
		self.chat_page = chat
		self.declared = False
		self.mydb = conn
		
	def on_release(self):
		if not self.declared:
			self.parent.parent.parent.parent.parent.parent.parent.parent.add_widget(ChatPage(name=self.chat_page, conn=self.mydb))
			
			self.declared = True
		
		self.parent.parent.parent.parent.parent.parent.parent.parent.current = self.chat_page
		

		
						
class TextWidget(Widget):
	text = StringProperty()
	def __init__(self, text='', **kwargs):
		super().__init__(**kwargs)
		self.text = text
		
class ProfilePage(Screen):
	details = OptionProperty('profile',options=['profile', 'friends', 'timeline'])
	gallery_sheet = None
	photo_sheet = None
	
	def __init__(self, user, conn, **kwargs):
		super(ProfilePage, self).__init__(**kwargs)
		self.mydb = conn
		self.user = user
		
		if self.details == 'timeline':
			self.ids['details'].default_tab = '2'
		elif self.details == 'friends':
			self.ids['details'].default_tab = '1'
		else:
			self.ids['details'].default_tab = '0'
		
		
	def change_profile_pic(self):
		self.open_gallery('pics')
		
			
	def open_gallery(self, opt):
		self.gallery_sheet = CustomGallerySheet(screen=Gallery(opt = opt, parentwidget = self, textwidget = self.ids['profile_pic'] ))
		self.gallery_sheet.open()
	
			
			
	def set_profile_pic(self):
		self.photo_sheet = EditDialog(
		content_cls= PhotoCropper(size_hint= (None, None), textwidget= self.ids['profile_pic'], size=(600, 600)),
		type= 'custom')
		self.photo_sheet.open()

		
		
class ChatPage(Screen):
	def __init__(self, conn, **kwargs):
		super(ChatPage, self).__init__(**kwargs)
		
	def goback(self):
		self.parent.current = 'mainscreen'
		
	def send_message(self):
		message = self.ids['message']
		self.ids['message'].text = ""
		Window.request_keyboard(target=message, callback='')
		
	def increase_for_keyb(self):
		self.ids['page_layout'].add_widget(BoxLayout(height=Window.keyboard_height), 4)
		


############################################################################################################



####################################
#                 LOGIN/REGISTRATION PAGE             #
####################################


class LoginScreen(ScreenManager):
	acolor = '#ffffff'
	bcolor= '#b2c95e'
	
	def __init__(self, conn ='', **kwargs):
		super(LoginScreen, self).__init__(**kwargs)
		self.mydb = conn
		
		
#######LOGIN TO MAINAPP##############
	def login(self):
		u = (self.ids.username.text).lower()
		p = self.ids.password.text
		log_cursor = self.mydb.cursor()
		log_cursor.execute("SELECT password, user_id FROM users WHERE username =%s or email =%s", (u,u))
		
		password, id = log_cursor.fetchone()
	
		if len(u)< 1:
			self.ids.log_error_mes.text =  "[color=#992211][i] Users Field Can't Be Empty[/i][/color]"
				
		elif len(p)< 1:
			self.ids.log_error_mes.text =  "[color=#992211][i]Password Field Can't Be Empty[/i][/color]"
			
		elif password == p:
			file = open('save.data','w')
			file.write('{}:{}'.format(u, id))
			appscreen = AppScreen(name='mainapp', conn = self.mydb, user = u, user_id = id)
			self.parent.parent.add_widget(appscreen)
			self.parent.parent.current = 'mainapp'
			self.parent.parent.remove_widget(self.parent)
			
		else:
			self.ids.log_error_mes.text =  "[color=#992211][i]Wrong Username \n Or Password[/i][/color]"
		
		
#######ERROR HANDLER###############
	def verify(self, page):
		if page == 1: #For Page 1
			s = self.ids.reg_surname.text
			f = self.ids.reg_firstname.text
				
			if not (re.search("[$#@]",s) or re.search("[0-9]",s) or re.search("[$#@]",f) or re.search("[0-9]",f) or re.search(' ',f) or re.search(' ',s) or len(s)<3 or len(s)>20 or len(f)<3 or len(f)>20):
				self.ids.reg_error_mes.text = ''
				return True
			else:
				self.ids.reg_error_mes.text =  "[color=#992211][i]Invalid Name[/i][/color]"
				
		if page == 2: #For Page 2
			if self.ids.gender.current_item is not '':
				return True
				
		if page == 3: #For Page 3
			u = (self.ids.reg_username.text).lower()
			e = (self.ids.reg_email.text).lower()
	
			ucursor = self.mydb.cursor()
			ucursor.execute("SELECT `username` FROM users WHERE username = %s", (u,))
			uresult = ucursor.fetchone()
				
			if re.search("[$#@]",u) or re.search(' ',u) or len(u)<2 or len(u)>20:
				self.ids.reg_error_mes.text =  "[color=#992211][i]Invalid Username[/i][/color]"
				
			elif not (re.search("@",e) and re.search(".c",e)) or re.search(' ',e) or len(e)<6 or len(e)>30:
				self.ids.reg_error_mes.text =  "[color=#992211][i]Invalid Email[/i][/color]"
				
			elif uresult == (u,):
				self.ids.reg_error_mes.text =  "[color=#992211][i]Username exist[/i][/color]"
				return False
				
			else:
				ecursor = self.mydb.cursor()
				ecursor.execute("SELECT `email` FROM users WHERE email = %s", (e,))
				eresult = ucursor.fetchone()
				
				if eresult == (e,):
					self.ids.reg_error_mes.text =  "[color=#992211][i]Email exist[/i][/color]"
					return False
				
				else:
					self.ids.reg_error_mes.text = ''
					return True
				
		if page == 4: #For Page 4
			self.ids.reg_error_mes.text = ''
			p = self.ids.reg_password.text
			c= self.ids.check_password.text
			
			if not (re.search("[A-Z]",p) or re.search("[a-z]",p) or re.search("[0-9]", p) or len(p)>7):
				self.ids.reg_error_mes.text =  "[color=#992211][i]Password is too weak \n (Enter at least one Upper Case, one Lower case and one Number) [/i][/color]"
				return False
				
			elif not (c == p):
				self.ids.reg_error_mes.text =  "[color=#992211][i]Passwords do not match[/i][/color]"
			
			elif (len(p)>30):
				self.ids.reg_error_mes.text =  "[color=#992211][i]Password too long[/i][/color]"
				
			else:
				self.ids.reg_error_mes.text = ''
				return True
			
			
							
				
			
######SWITCH REGISTRATION PAGE#######
	def switch_reg_page(self):
		error = self.ids.reg_error_mes.text
		if self.ids.login.text == 'Next':
			
			if self.ids.reg_step.current == 'first_reg_page' and self.verify(1):
				self.reg_error_mes = ''
				self.ids.reg_step.current = 'second_reg_page'
				
			elif self.ids.reg_step.current == 'second_reg_page' and self.verify(2):
				self.reg_error_mes = ''
				self.ids.reg_step.current = 'third_reg_page'
				
			elif self.ids.reg_step.current == 'third_reg_page' and self.verify(3):
				self.reg_error_mes = ''
				self.ids.reg_step.current = 'fourth_reg_page'
				self.ids.login.text = 'Sign Up'
				
		elif self.ids.login.text == 'Sign Up' and self.verify(4):
				self.signup()
				self.ids.username.text = self.ids.reg_username.text
				self.ids.password.text = self.ids.reg_password.text
				self.current = 'login'
			
######CONVERT STR MONTH TO INT#######
	def conmonth(self, mon):
		loop = ['January', 'february', 'March',  'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		num = 0
		for i in loop:
			num = num + 1
			if i == mon:
				break
				
		return num
			
######RETURN LAST YEAR TO 1960########
	def year(self):
		thisyear = datetime.today().year
		year = []
		for i in range(thisyear-1960):
			year.append(str(thisyear-(i+1)))
		return year
		
		
		
#######RETURN ALL MONTH IN A YEAR####
	def month(self):
		mon = ['January', 'february', 'March',  'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		return mon
		
		
#######RETURN DAYS IN A MONTH########
	def day(self,m, y):
		day = []
		m = self.conmonth(m)
		try:
			if m == 9 or m == 4 or m == 6 or m == 11:
				for i in range(30):
					day.append(str(i+1))
			elif m == 2 and int(y) % 4 == 0:
				for i in range(29):
					day.append(str(i+1))
			elif m == 2 and (int(y) %4) is not 0:
				for i in range(28):
					day.append(str(i+1))
			else:
				for i in range(31):
					day.append(str(i+1))
		except:
			for i in range(30):
				day.append(str(i+1))
				
		return day
					      
			      
####SWITCH PASSWORD SEEN CASE#######
	def switch_seen(self):
		if self.ids.see_password.icon == 'eye':
			self.ids.see_password.icon = 'eye-off'
			self.ids.password.password = False
		else:
			self.ids.see_password.icon = 'eye'
			self.ids.password.password = True
			
###SWITCH PASSWORD SEEN CASE IN REG##
	def switch_seen2(self):
		if self.ids.see_reg_password.icon == 'eye':
			self.ids.see_reg_password.icon = 'eye-off'
			self.ids.reg_password.password = False
			self.ids.check_password.password = False
		else:
			self.ids.see_reg_password.icon = 'eye'
			self.ids.reg_password.password = True
			self.ids.check_password.password = True
			
###TO SIGNUP AND SEND DATA TO DB######
	def signup(self):
		month = self.conmonth(self.ids.month.current_item)
		
		year = int(self.ids.year.current_item)
		day = int(self.ids.day.current_item)
		f_name = (self.ids.reg_firstname.text).lower()
		s_name = (self.ids.reg_surname.text).lower()
		u_name = (self.ids.reg_username.text).lower()
		
		gender = (self.ids.gender.current_item).lower()
		
		email = (self.ids.reg_email.text).lower()
		
		passwd= self.ids.reg_password.text
		
		d_birth = date(year, month, day)
		
#		age = int((date.today() - d_birth).days/365.2425)
		reg_date = datetime.today()
		
		
		

		reg_cursor = self.mydb.cursor()
		value1 = (u_name, email, passwd)
		value2 =  (f_name, s_name, u_name, email, gender, d_birth, reg_date )
		
		query1 = '''
INSERT INTO users( `username`, `email`, `password` ) VALUES ( %s, %s, %s);
'''

		query2 = '''
INSERT INTO profile(`first_name`, `surname`, `username`, `email`, `gender`, `date_of_birth`, `reg_date`) VALUES ( %s, %s, %s, %s, %s, %s, %s);
	'''
		result1 = reg_cursor.execute(query1, value1)
		result2 = reg_cursor.execute(query2, value2)
		
####################################
#           DEFAULT BACKGROUND CLASS            #
####################################

class Background(ScreenManager):
	def __init__(self, **kwargs):
		super(Background, self).__init__(**kwargs)
		self.mydb = mc.connect(host='127.0.0.1', user='root', passwd='', database='smartapp')
		
		try:
			file = open('save.data','r')
			u, id = (file.read()).split(':',1)
			appscreen = AppScreen(name='mainapp', conn = self.mydb, user = u, user_id = id)
			self.add_widget(appscreen)
			self.current = 'mainapp'
		except:
			loginscreen = LoginScreen(conn =self.mydb)
			signin = Screen(name='loginpage')
			signin.add_widget(loginscreen)
			self.add_widget(signin)
			self.current = 'loginpage'
	
	
class mainapp(MDApp):
	def build(self):
		self.theme_cls.primary_palette = 'Gray'
		self.theme_cls.theme_style = 'Dark'
		return Background()
		
if __name__ == '__main__':
	mainapp().run()