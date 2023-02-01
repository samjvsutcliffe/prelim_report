(restrict-compiler-policy 'speed 3 3)
(restrict-compiler-policy 'debug 0 0)
(restrict-compiler-policy 'safety 0 0)
;(setf *block-compile-default* t)
;(push :magicl.use-mkl *features*)
(ql:quickload "magicl")
(ql:quickload "cl-mpm")
(ql:quickload "cl-mpm/examples/notch")
(in-package :cl-mpm/examples/notch)

(defun rectangle-sdf (position size)
  (lambda (pos)
      (let* ((position (magicl:from-list position '(2 1) :type 'double-float))
             (dist-vec (magicl:.- (magicl:map! #'abs (magicl:.- pos position))
                                  (magicl:from-list size '(2 1) :type 'double-float))))

        (+ (sqrt (magicl::sum
                  (magicl:map! (lambda (x) (* x x))
                               (magicl:map! (lambda (x) (max 0d0 x)) dist-vec))))
           (min (max (magicl:tref dist-vec 0 0)
                     (magicl:tref dist-vec 1 0)
                     ) 0d0)))))

(defun setup-test-column (size block-size block-offset &optional (e-scale 1d0) (mp-scale 1d0)
                          &rest mp-args)
  (let* ((sim (cl-mpm/setup::make-block (/ 1 e-scale)
                                        (mapcar (lambda (s) (* s e-scale)) size)
                                        #'cl-mpm/shape-function:make-shape-function-bspline)) 
         (h (cl-mpm/mesh:mesh-resolution (cl-mpm:sim-mesh sim)))
         ;(e-scale 1)
         (h-x (/ h 1d0))
         (h-y (/ h 1d0))
         (density 900)
         ;; (mass (/ (* 900 h-x h-y) (expt mp-scale 2)))
         (elements (mapcar (lambda (s) (* e-scale (/ s 2))) size)))
    (progn
      (let ((block-position
              (mapcar #'+ (list (* h-x (- (+ (/ 1 (* 2 mp-scale))) 0))
                                (* h-y (+ (/ 1d0 (* 2d0 mp-scale)))))
                      block-offset)))
        (setf (cl-mpm:sim-mps sim)
              (cl-mpm/setup::make-block-mps
               block-position
               block-size
               (mapcar (lambda (e) (* e e-scale mp-scale)) block-size)
               density
               'cl-mpm::make-particle
                'cl-mpm/particle::particle-elastic
                ;'cl-mpm/particle::particle-viscoplastic
                ;'cl-mpm/particle::particle-elastic-damage
                 :E 1d9
                 :nu 0.3250d0
                 ;:visc-factor 111d6
                 ;:visc-power 3d0
                 ;:critical-stress 1d6
                 :gravity -9.8d0
                 ;; :gravity-axis (magicl:from-list '(0.5d0 0.5d0) '(2 1))
                 :index 0
               )))
      (setf (cl-mpm:sim-damping-factor sim) 0.1d0)
      (setf (cl-mpm:sim-mass-filter sim) 1d-15)
      (setf (cl-mpm::sim-allow-mp-split sim) nil)
      (setf (cl-mpm::sim-enable-damage sim) nil)
      (setf (cl-mpm::sim-allow-mp-damage-removal sim) nil)
      (setf (cl-mpm:sim-dt sim) 1d-2)
      (setf (cl-mpm:sim-bcs sim)
            (append
             (cl-mpm/bc::make-outside-bc-var
              (cl-mpm:sim-mesh sim)
              (lambda (i) (cl-mpm/bc:make-bc-fixed i '(0 nil)))
              (lambda (i) (cl-mpm/bc:make-bc-fixed i '(0 nil)))
              (lambda (i) (cl-mpm/bc:make-bc-fixed i '(nil 0)))
              (lambda (i) (cl-mpm/bc:make-bc-fixed i '(nil 0)))
              )
             )
            )
      ;(setf (cl-mpm::sim-bcs-force sim)
      ;      (cl-mpm/bc:make-bcs-from-list
      ;        (list (cl-mpm/bc::make-bc-closure '(0 0)
      ;                                          (lambda ()
      ;                                            (cl-mpm/buoyancy::apply-bouyancy sim 300d0))))))

       (let ((ocean-x 0)
             (ocean-y 300))
         (setf (cl-mpm::sim-bcs-force sim)
               (cl-mpm/bc:make-bcs-from-list
                 (loop for x from (floor ocean-x h) to (floor (first size) h)
                       append (loop for y from 0 to (floor ocean-y h)
                                    collect (cl-mpm/bc::make-bc-buoyancy
                                              (list x y)
                                              (magicl:from-list (list 0d0 (* 9.8d0 (* 1.0d0 1000))) '(2 1)))))))
         )
      sim)))

;Setup
(defun setup ()
  (let* ((shelf-length 2000)
         (shelf-height 200)
         (shelf-bottom 120)
         (notch-length 100)
         (notch-depth 30)
         )
    (defparameter *sim* (setup-test-column (list (+ 100 shelf-length) 400)
                                           (list shelf-length shelf-height)
                                           (list 0 shelf-bottom) (/ 1 25) 4))
    (remove-sdf *sim* (rectangle-sdf (list shelf-length (+ shelf-height shelf-bottom)) (list notch-length notch-depth)))
    )
  (defparameter *velocity* '())
  (defparameter *time* '())
  (defparameter *t* 0)
  (defparameter *x* 0)
  (defparameter *x-pos* '())
  (defparameter *sim-step* 0)
  (defparameter *run-sim* nil)
  (defparameter *run-sim* t)
  (defparameter *notch-position* 0.1d0)
  (defparameter *load-mps*
    (let* ((mps (cl-mpm:sim-mps *sim*))
           (least-pos
              (apply #'max (loop for mp across mps
                                 collect (magicl:tref (cl-mpm/particle:mp-position mp) 0 0)))))
      (loop for id from 0 to (- (length mps) 1) when (>= (magicl:tref (cl-mpm/particle:mp-position (aref mps id)) 0 0) (- least-pos 0.001))
              collect (aref mps id))))
  )


(defparameter *run-sim* nil)

(defun run ()
  (cl-mpm/output:save-vtk-mesh (merge-pathnames "output/mesh.vtk")
                          *sim*)
  (defparameter *run-sim* t)
  (let* ((ms (cl-mpm/mesh::mesh-mesh-size (cl-mpm:sim-mesh *sim*)))
         (ms-x (first ms))
         (ms-y (second ms))
         ))
  (setf *x* 
    (loop for mp across (cl-mpm:sim-mps *sim*)
        maximize (magicl:tref (cl-mpm/particle:mp-position mp) 0 0)))
  (with-open-file (stream (merge-pathnames "output/terminus_position.csv") :direction :output :if-exists :supersede)
    (format stream "Time (s),Terminus position~%")
    (format stream "~f, ~f ~%" *t* *x*)
    )
     
    (time (loop for steps from 0 to 100
                while *run-sim*
                do
                (progn
                  ;(push *t* *time*)
                  ;(setf *x* 
                  ;  (loop for mp across (cl-mpm:sim-mps *sim*)
                  ;        maximize (magicl:tref (cl-mpm/particle:mp-position mp) 0 0)))
                  ;(push *x*
                  ;  *x-pos*)
                  (format t "Step ~d ~%" steps)

                  (cl-mpm/output:save-vtk (merge-pathnames (format nil "output/sim_~5,'0d.vtk" *sim-step*)) *sim*)
                  (cl-mpm/output:save-csv (merge-pathnames (format nil "output/simcsv_~5,'0d.vtk" *sim-step*)) *sim*)
                  (incf *sim-step*)
                  (time (dotimes (i 100)
                          (cl-mpm::update-sim *sim*)
                          ;(remove-sdf *sim* (rectangle-sdf (list 2000 330) (list *notch-position* 30)))
                          ;(incf *notch-position* (* (cl-mpm:sim-dt *sim*) 5d0))
                          (setf *t* (+ *t* (cl-mpm::sim-dt *sim*)))
                          ))
                  )))
    (cl-mpm/output:save-vtk (merge-pathnames (format nil "output/sim_~5,'0d.vtk" *sim-step*)) *sim*)
                  (cl-mpm/output:save-csv (merge-pathnames (format nil "output/simcsv_~5,'0d.vtk" *sim-step*)) *sim*)
  
;;  (with-open-file (stream (merge-pathnames "output/terminus_position.csv") :direction :output :if-exists :supersede)
;;    (format stream "Time (s), Terminus position~%")
;;    (loop for tim in (reverse *time*)
;;          for x in (reverse *x-pos*)
;;          do (format stream "~f, ~f ~%" tim x)))
  
  )


(setf lparallel:*kernel* (lparallel:make-kernel 32 :name "custom-kernel"))
(require :sb-sprof)
(defparameter *run-sim* nil)
(setup)
(format t "MP count:~D~%" (length (cl-mpm:sim-mps *sim*)))
(run)
;(run)
;(sb-sprof:start-profiling)
;  (time 
;    (dotimes (i 1000)
;      (cl-mpm::update-sim *sim*)))

;  (time 
;    (lparallel:pdotimes (i 100000)
;                        (let ((m  (magicl:zeros '(2 2))))
;                          (magicl:eig m))))
;  (time
;    (dotimes (i 100000)
;      (let ((m  (magicl:zeros '(2 2))))
;        (magicl:eig m))))
        
 (defmacro time-form (form it)
   `(progn
     (declaim (optimize speed))
     (let* ((iterations ,it)
            (start (get-internal-real-time)))
       (dotimes (i iterations) ,form)
       (let* ((end (get-internal-real-time))
              (units internal-time-units-per-second)
              (dt (/ (- end start) (* iterations units)))
              )
         (format t "Total time: ~f ~%" (/ (- end start) units)) (format t "Time per iteration: ~f~%" (/ (- end start) (* iterations units)))
         (format t "Throughput: ~f~%" (/ 1 dt))
         dt))))
;;
(defparameter *threads* '())
(defparameter *times* '())
;(loop for k in '(1 2 4 8 16 32)
;      do (progn
;           (push k *threads*)
;           (setf lparallel:*kernel* (lparallel:make-kernel k :name "custom-kernel"))
;           ;(sb-sprof:start-profiling)
;           (with-accessors ((mesh cl-mpm:sim-mesh)
;                            (mps cl-mpm:sim-mps)
;                            (dt cl-mpm:sim-dt))
;             *sim*
;             (format t "Threads ~D~%" k)
;             (setup)
;             (let ((tim (time-form 
;                          ;(cl-mpm::p2g mesh mps)
;                          ;(cl-mpm::update-stress mesh mps dt)
;                          (cl-mpm::update-sim *sim*)
;                                   100)))
;               (push tim *times*))
;             ;(time (dotimes (i 100)
;             ;        (cl-mpm::update-stress mesh mps dt)
;             ;        ))
;             
;             )))
;(with-open-file (stream (merge-pathnames "throughputs.csv") :direction :output :if-exists :supersede)
;    (format stream "threads,time~%")
;    (loop for tim in (reverse *threads*)
;          for x in (reverse *times*)
;          do (format stream "~f, ~f ~%" tim x)))
;(sb-sprof:stop-profiling)
;(sb-sprof:report :type :flat)
(room)
