# encoding:utf-8

import tkinter as tk, os
import matplotlib, cv2
import numpy as np

import filterandpass as fltr

matplotlib.use('TkAgg') 

from matplotlib import pyplot as plt, animation 
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
    
        self.title('Image Filter App')
        self.geometry("1920x1080")
        self.filter_type = tk.StringVar()
        self.pass_type = tk.StringVar()
        self.current_value = tk.DoubleVar()
        self.selected_size = tk.StringVar()
        self.slider_type = tk.DoubleVar()
        

        plot_button = tk.Button(master = self, 
                     command = self.loadImage,
                     height = 2, 
                     width = 10,
                     text = "Load Image")


        self.filter_now = "None"
        self.pass_now = "None"
        self.slider_now = 1
        self.load_img_status = False

        self.orj_img = np.zeros([100,100,3],dtype=np.uint8)
        self.filtered_img = np.zeros([100,100,3],dtype=np.uint8)
        self.filter = np.zeros([100,100,3],dtype=np.uint8)
        self.dvu = 0
        self.h = 0
        
        self.figureX = plt.figure(figsize=(3, 3), dpi=100)
        self.figureY = plt.figure(figsize=(3, 3), dpi=100)
        self.figureZ = plt.figure(figsize=(3, 3), dpi=100)
        self.figureK = plt.figure(figsize=(3, 3), dpi=100)

        self.figure_canvasX = FigureCanvasTkAgg(self.figureX, self)
        self.figure_canvasY = FigureCanvasTkAgg(self.figureY, self)
        self.figure_canvasZ = FigureCanvasTkAgg(self.figureZ, self)
        self.figure_canvasK = FigureCanvasTkAgg(self.figureK, self)

        self.axes1 = self.figureX.add_subplot()
        self.axes2 = self.figureY.add_subplot()
        self.axes3 = self.figureZ.add_subplot()
        self.axes4 = self.figureK.add_subplot()

        self.axes1.axis('off')
        self.axes2.axis('off')
        self.axes3.axis('off')

        self.figureX.set_facecolor((0.94, 0.94, 0.94))
        self.figureY.set_facecolor((0.94, 0.94, 0.94))
        self.figureZ.set_facecolor((0.94, 0.94, 0.94))
        self.figureK.set_facecolor((0.94, 0.94, 0.94))

        self.axes1_data = self.axes1.imshow(self.orj_img, cmap="gray")
        self.axes2_data = self.axes2.imshow(self.filter, cmap="gray")
        self.axes3_data = self.axes3.imshow(self.filtered_img, cmap="gray")
        self.axes1_data.set_clim(vmin=0, vmax=255)
        self.axes4.plot(0,0, 'g')

        self.figure_canvasX.draw()
        self.figure_canvasY.draw()
        self.figure_canvasZ.draw()
        self.figure_canvasK.draw()

        self.figure_canvasX.get_tk_widget().grid(row=0, column=0, ipadx=10, ipady=10)
        self.figure_canvasY.get_tk_widget().grid(row=0, column=1, ipadx=10, ipady=10)
        self.figure_canvasZ.get_tk_widget().grid(row=1, column=2, ipadx=10, ipady=10)
        self.figure_canvasK.get_tk_widget().grid(row=0, column=2, ipadx=10, ipady=10)
        
        self.slider = tk.Scale(
            self,
            from_=1,
            to=250,
            length = 250,
            digits = 4,
            resolution = 1.0,
            orient='horizontal',
            variable=self.slider_type,
            command=self.sliderCallback
        )

        filter1 = tk.Radiobutton(self, width=0, height= 0, text="Ideal", variable=self.filter_type, value="ideal", command=self.filterCallback)
        filter2 = tk.Radiobutton(self, text="BTW", variable=self.filter_type, value="butterworth", command=self.filterCallback)
        filter3 = tk.Radiobutton(self, text="Gaussian", variable=self.filter_type, value="gaussian", command=self.filterCallback)
        self.hpf_radio = tk.Radiobutton(self, text="HPF", variable=self.pass_type, value="hpf", command=self.passCallback)
        self.lpf_radio = tk.Radiobutton(self, text="LPF", variable=self.pass_type, value="lpf", command=self.passCallback)
        
        self.lpf_radio.configure(state= tk.DISABLED)
        self.hpf_radio.configure(state= tk.DISABLED)
        filter1.place(x=40, y=800)
        filter2.place(x=40, y=820)
        filter3.place(x=40, y=840)
        plot_button.place(x=40, y=880)
        self.hpf_radio.place(x=200, y=800)
        self.lpf_radio.place(x=200, y=820)
        self.slider.place(x=40, y=700)       
        
        self.ani = animation.FuncAnimation(self.figureX, self.updateRender, interval=1000)

    def passCallback(self):
        self.pass_now = self.pass_type.get()

    def filterCallback(self):
        
        self.lpf_radio.configure(state= tk.NORMAL)
        self.hpf_radio.configure(state= tk.NORMAL)
        
        self.filter_now = self.filter_type.get()


    def sliderCallback(self, event):
        self.slider_now = self.slider.get()
        

    def controlInputs(self):
        if (self.filter_now != "None" and self.load_img_status and self.pass_now != "None"):
            return True
        else:
            return False

    def to_raw(self, string):
        return r"{string}"
    
    def loadImage(self):
        
        file_path= tk.filedialog.askopenfilename(title = "Select A File", filetypes = (("jpg", "*.jpg"), ("png", "*.png"), ("jpeg", "*.jpeg")))
        file_path = file_path.encode('utf-8').decode('utf-8').replace('/', '\\\\')               # For Windows Absoulate Path
        raw_image = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)   # For unicode chars
        raw_image = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)                                                     
        raw_image = cv2.resize(raw_image,(250, 250))
        self.orj_img = raw_image
        self.load_img_status = True
        #self.updateRender()

    def updateRender(self, event):
        
        plt.cla()

        self.calculeFilter()
        
        self.axes1_data.set_data(self.orj_img)
        self.axes2_data.set_data(self.filter)
        self.axes3_data.set_data(self.filtered_img)

        self.axes2_data.autoscale()
        self.axes3_data.autoscale()

        self.axes4.set_title('Graphic of Filter')
        self.axes4.set_xlabel("D(u,v)")
        self.axes4.set_ylabel("H(u,v)")
        self.axes4.plot(self.dvu,self.h, 'b')
        
        self.figure_canvasX.draw()
        self.figure_canvasY.draw()
        self.figure_canvasZ.draw()
        self.figure_canvasK.draw()

        self.figure_canvasX.flush_events()
        self.figure_canvasY.flush_events()
        self.figure_canvasZ.flush_events()
        self.figure_canvasK.flush_events()
        #return self.filter    
        #self.after(1,self.updateRender)

    def calculeFilter(self):
        
        if self.controlInputs():
            img_float32=np.float32(self.orj_img)
            filters = fltr.filter(5)
            filters.updateImage(self.orj_img)
            dvu = filters.computeDuv()
            h = filters.computeH(self.filter_now, self.pass_now, self.slider_now, dvu)

            fftimg = filters.computeFFT(img_float32)
            fftfiltered = filters.applyFilter(fftimg, h)
            filtered_image = filters.computeInverseFFT(fftfiltered)
            
            self.dvu = dvu
            self.h = h
            self.filter = h
            self.filtered_img = filtered_image

if __name__ == '__main__':
    app = App()
    app.mainloop()
    
