from kivy.uix.scatter import Scatter
from kivymd.uix.imagelist import SmartTile
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.core.image import Image as CoreImage
from kivy.uix.scatter import Scatter
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import BackgroundColorBehavior

from kivy.properties import OptionProperty, ObjectProperty, StringProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout

from kivy.effects.dampedscroll import DampedScrollEffect
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.app import MDApp
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.lang import Builder
from PIL import Image
import glob
from time import time
import os

KV = '''
#: import rgba kivy.utils.get_color_from_hex
#: import ScrollEffect kivy.effects.scroll.ScrollEffect

<Gallery>:
	cols: 1
	size_hint: 1, None
	height: 725
	padding: dp(5), dp(15), dp(5), dp(15)
	GalleryScrollView:
		root_widget: root
		scroll_type: ['bars', 'content']
		ImagesHolder:
			id: image_holder
			cols: 1
			size_hint_y: None
			adaptive_height: False
			GridLayout:
				id: all_images
				size_hint: 1, 1
				cols: 3


<ScatterImage@Image+Scatter>

<GalleryImage>:
	size_hint: 1, None
	height: self.width
	allow_stretch: False
	lines: 2
	box_color: (0,0,0,0)
	
<ImagesHolder@BackgroundColorBehavior+GridLayout>


<CustomGallerySheet>:
	duration_opening: .2
	radius: dp(20)
	radius_from: 'top'
	height: 725
	animation: True
	
<ScatterImage@Scatter+Image>
	
<PhotoCropper>:
	orientation: 'vertical'
	size_hint: 1, None
	height: self.width
	
	RelativeLayout:
		size_hint: None, None
		size: root.width, root.width
		canvas.after:
			Color:
				rgba: (0, 0, 0, .4)
			Line:
				width: 600
				circle: (self.center_x, self.center_y, 850, 0, 360)
		ScatterImage:
			id: selected
			do_rotation: False
			pos_hint: {'center_x': 0.5, 'center_y': 0.5}
			
	FloatLayout:
		size_hint_y: None
		height: 0
		MDFloatingActionButton:
			icon: 'checkbox-marked'
			pos_hint: {'center_x': 0.15, 'y': root.width/10}
			md_bg_color: app.theme_cls.primary_color
			on_release: root.save_photo(selected.source)
		MDFloatingActionButton:
			icon: 'cancel'
			pos_hint: {'center_x': 0.85, 'y':root.width/10}
			md_bg_color: app.theme_cls.primary_color
			
			
'''
Builder.load_string(KV)

####################################
#                   FLOATING GALLERY                          #
####################################



class GalleryImage(SmartTile, ButtonBehavior):
	def __init__(self, **kwargs):
		super(GalleryImage, self).__init__(**kwargs)
		
	def on_release(self):
		
		self.parent.parent.parent.parent.parentwidget.gallery_sheet.dismiss()
		
		self.parent.parent.parent.parent.textwidget.text = self.source
		
		self.parent.parent.parent.parent.parentwidget.set_profile_pic()
		
#######GALLERY THAT HOLDS ALL########

class Gallery(GridLayout):
	dir = '/sdcard/'
	load_limit = 0
	images = []
	
	img_len = NumericProperty()
	opt = OptionProperty('all', options=['pics', 'vids', 'all'])
	parentwidget = ObjectProperty()
	textwidget = ObjectProperty()
	
	def __init__(self, opt, parentwidget, textwidget, **kwargs):
		super(Gallery, self).__init__(**kwargs)
		self.opt = opt
		self.parentwidget = parentwidget
		self.textwidget = textwidget
		
		self.load_limit = 0
		self.images = []
		
		def start(interval):
			self.set_condition()
			self.images.sort(key= lambda x: os.path.getmtime(x), reverse=True)
			
			self.page_len = (len(self.images)/3) * 225
			self.ids['image_holder'].height = self.page_len
			
			self.add_images()

		Clock.schedule_once(start, 0.5)
		
#####VIEW IMAGES FROM SOURCE########
		
	def add_images(self):
		h = 225
		l = self.load_limit 
		
		for image in self.images[l: l+9]:
			self.load_limit = self.load_limit + 1
			self.ids['all_images'].add_widget(GalleryImage(source=image))
		
		l = self.load_limit /3


######CONDITION FOR SELECTION########

	def set_condition(self):
		if self.opt == 'pics':
			for r, d, f in os.walk(self.dir):
				for file in f:
					if file.endswith(".png") or file.endswith(".jpg"):
						self.images.append(os.path.join(r, file))			
		elif self.opt == 'vids':
			for r, d, f in os.walk(self.dir):
				for file in f:
					if file.endswith(".mp4") or file.endswith(".3gp"):
						self.images.append(os.path.join(r, file))
		else:
			for r, d, f in os.walk(self.dir):
				for file in f:
					if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".mp4") or file.endswith(".3gp"):
						self.images.append(os.path.join(r, file))
		self.img_len = len(self.images)
						
######POP UP SHEET FOR GALLERY######			
						

class CustomGallerySheet(MDCustomBottomSheet):
	screen = ObjectProperty()
	def __init__(self, **kwargs):
		super(CustomGallerySheet, self).__init__(**kwargs)
		self.height = self.screen.height
		


######SCROLL EFFECT AND BEHAVIOR#####

class GalleryScrollEffect(DampedScrollEffect):
	max_screen_to_reload = NumericProperty('100')
	
	def on_scroll(self, scrollview, overscroll):
		scroll_view = self.target_widget.parent
		scroll_view._max_scrolled = True
	

class GalleryScrollView(ScrollView):
	root_widget = ObjectProperty()
	thevar = 3
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.effect_cls = GalleryScrollEffect
		self._max_scrolled = False
		
	def on_touch_down(self, *args):
		position, size = self.vbar
		if not self._max_scrolled or ((1 - position)*self.root_widget.img_len) > (self.root_widget.ids['all_images'].width/3 * self.thevar):
			self._max_scrolled = False
		else:
			self.thevar = self.thevar + 1
			self.root_widget.add_images()
			
		return super().on_touch_down(*args)

 
	
####################################
####################################
####################################

class EditDialog(MDDialog):
	parent_cls = ObjectProperty()
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		
		self.size_hint=(1, None)
		self.height= self.width
		self.pos_hint= {'center_x': 0.5, 'center_y': 0.75}
		self.radius=[20, 7, 20, 7]
        
        
class PhotoCropper(BoxLayout, BackgroundColorBehavior):
	textwidget = ObjectProperty()
	
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.ids['selected'].source = self.textwidget.text
		self.md_bg_color= [.2, .2, .2, .6]
		
#	def set_image(self):
		img = self.ids['selected'].size
		img_w, img_h = self.ids['selected'].size
		if min(img) < 500:
			if min(img) == img_w:
				self.ids['selected'].width = 500
				self.ids['selected'].height = (max(img)/min(img))* 500
				
			elif min(img) == img_h:
				self.ids['selected'].height= 500
				self.ids['selected'].width = (max(img)/min(img))* 500
				
		
	def save_photo(self, img_source):
		image = Image.open(img_source)
		img_width, img_height = image.size
		crop_img = image.crop((
			img_width-min(image.size) // 2,
			img_height-min(image.size) //2,
			img_width+min(image.size) //2,
			img_height+min(image.size) //2))
		crop_img.save('icon2.png', quality= 95)
			
		self.textwidget.text = 'icon2.png'