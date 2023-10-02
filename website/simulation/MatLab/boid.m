classdef boid
    properties
        pos
        vel
        acc
        max_speed
    end
    methods
        function obj = boid(pos_x, pos_y)
            obj.acc = [0, 0];

            angle = (2*pi)*rand;
            obj.vel = [cos(angle), sin(angle)]

            obj.pos = [pos_x, pos_y]
            obj.max_speed = 2
        end

        function obj = update()
            obj.vel = obj.vel + obj.acc
            obj.pos = obj.pos + norm(obj.vel + ((1/2)*obj.acc))*obj.max
            obj.acc = [0, 0]
        end
    end
end

